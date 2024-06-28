class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
  before_action :authenticate_user

  def my_logger
    @@my_logger ||= Logger.new("#{Rails.root}/log/#{Rails.env.to_s}_errors.log")
  end


  def authenticate_user
    if not cookies[:jwt]
      redirect_to "/login"
    else
      begin
        @data = JWT.decode cookies[:jwt], Rails.application.secrets[:jwt_key], true, { :algorithm => 'HS256' }
        @user = User.find_by_id!(@data[0]['user_id'])
      rescue => exception
        # Handle invalid token
        cookies.delete :jwt
        my_logger.error("error: #{exception.to_s}")
        redirect_to "/login", :flash => { :error => "Invalid Session" }
      end
    end
  end
  
  
end
