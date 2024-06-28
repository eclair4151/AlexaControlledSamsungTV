class ChooseDeviceController < ApplicationController
  skip_before_action :authenticate_user
  layout 'root'
  
  
  def index
    @state = params[:state]
    @redirect_uri = params[:redirect_uri]
    @jwt = params[:jwt]
    begin
        data = JWT.decode params[:jwt], Rails.application.secrets[:jwt_key], true, { :algorithm => 'HS256' }
        user = User.find_by_id!(data[0]['user_id'])
        @devices = user.devices.where(:deleted => false).order(:created_at)

      rescue => exception
        # Handle invalid token
        cookies.delete :jwt
        my_logger.error("error: #{exception.to_s}")
        redirect_to "/alexa_login?state=" + params[:state] + '&redirect_uri=' + params[:redirect_uri], :flash => { :error => "Invalid Session" }
      end
  end


  def create
     begin
        data = JWT.decode params[:jwt], Rails.application.secrets[:jwt_key], true, { :algorithm => 'HS256' }
        user = User.find_by_id!(data[0]['user_id'])
        
        device = user.devices.find_by_uuid!(params[:id])
        jwt_payload = {user_id: user.id, device_uuid: device.uuid}
        token = JWT.encode jwt_payload, Rails.application.secrets[:jwt_key], 'HS256'
        redirect_to params[:redirect_uri] + '?state=' + params[:state] + '&code=' + token
      rescue => exception
        # Handle invalid token
        cookies.delete :jwt
        my_logger.error("error: #{exception.to_s}")
        redirect_to "/alexa_login?state=" + params[:state] + '&redirect_uri=' + params[:redirect_uri], :flash => { :error => "Invalid Session" }
      end
   
  end

end