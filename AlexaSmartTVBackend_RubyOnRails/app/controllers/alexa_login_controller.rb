class AlexaLoginController < ApplicationController
  skip_before_action :authenticate_user
  layout 'root'
  
  def index
    @state = params[:state]
    @redirect_uri = params[:redirect_uri]
  end
  
  def create
    
    user = User.find_by_email(params[:email].strip.downcase)
    if user!= nil and user.authenticate(params[:password])
      if user.devices.count == 0
        redirect_to '/alexa_login?state=' + params[:state] + '&redirect_uri=' + params[:redirect_uri], :flash => { :error => "This account does not have any devices registered with it." }
      elsif user.devices.count > 1
        jwt_payload = {user_id: user.id}
        token = JWT.encode jwt_payload, Rails.application.secrets[:jwt_key], 'HS256'
        redirect_to '/choose_device?jwt=' + token + '&redirect_uri=' + params[:redirect_uri] + '&state=' + params[:state]
      else
        jwt_payload = {user_id: user.id, device_uuid: user.devices.where(deleted: false).first.uuid}
        token = JWT.encode jwt_payload, Rails.application.secrets[:jwt_key], 'HS256'
        redirect_to params[:redirect_uri] + '?state=' + params[:state] + '&code=' + token#, :overwrite_params => { :state => params[:state], :code => token}

      end
    else
      redirect_to '/alexa_login?state=' + params[:state] + '&redirect_uri=' + params[:redirect_uri], :flash => { :error => "Incorrect Username or Password" }
    end
  
  end
end
