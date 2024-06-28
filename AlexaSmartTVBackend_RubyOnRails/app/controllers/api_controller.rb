class ApiController < ActionController::API
  before_action :authenticate_user
  before_action :validate_schema, only: [:create]


  rescue_from StandardError do |exception|
    my_logger.error("error: #{exception.to_s}")
    my_logger.error("backtrace: #{exception.backtrace.join("\n")}")
    
    if Rails.env.production?
      render :json => ErrorGen.create_error(500,'an unknown error occurred')
    else
      render :json => ErrorGen.create_error(500,exception.to_s)
    end

  end


  rescue_from ActiveRecord::RecordNotFound do |exception|
    my_logger.error("error: #{exception.to_s}")

    if Rails.env.production?
      render :json => ErrorGen.create_error(404,'item not found')
    else
      render :json => ErrorGen.create_error(404,exception.to_s)
    end
  end


  def my_logger
    @@my_logger ||= Logger.new("#{Rails.root}/log/#{Rails.env.to_s}_errors.log")
  end

 
  def authenticate_user
    begin
      @data = JWT.decode request.headers['jwt'], Rails.application.secrets[:jwt_key], true, { :algorithm => 'HS256' }
      @user = User.find_by_id!(@data[0]['user_id'])

    rescue => exception
      # Handle invalid token
      my_logger.error("error: #{exception.to_s}")

      if Rails.env.production?
        render :json => ErrorGen.create_error(401,'invalid session')
      else
        render :json => ErrorGen.create_error(401,exception.to_s)
      end
      false
    end
  end


  def validate_schema
    if not JSON::Validator.validate(SchemaValidator.get_schema(controller_name), params.as_json)
      if Rails.env.production?
        my_logger.error("error: #{controller_name}")
        render :json => ErrorGen.create_error(400,'invalid input')
      else
        error = JSON::Validator.fully_validate(SchemaValidator.get_schema(controller_name), params.as_json).to_s
        my_logger.error("error: #{error}")
        render :json => ErrorGen.create_error(400,'input json did not match schema: ' + error)
      end
      false
    end
  end

end