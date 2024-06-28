class Api::V1::LoginController < ApiController
    skip_before_action :authenticate_user

    def create
        user = User.find_by_email(params[:email].strip.downcase)
	if user!= nil and user.authenticate(params[:password])
          jwt_payload = {user_id: user.id}
          token = JWT.encode jwt_payload, Rails.application.secrets[:jwt_key], 'HS256'
          render json: {jwt: token}
        else
          render json: ErrorGen.create_error(401,'Username or password is incorrect')
        
        end
    end
 
end
