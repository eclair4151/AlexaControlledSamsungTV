class Api::V1::GetDevicesController < ApiController

    def create
        device = @user.devices.find_by_uuid!(params[:uuid])
        
        
        render json: {tvs: device.tvs.as_json(:except => [:created_at, :updated_at, :device_id])}
    end
       
end
