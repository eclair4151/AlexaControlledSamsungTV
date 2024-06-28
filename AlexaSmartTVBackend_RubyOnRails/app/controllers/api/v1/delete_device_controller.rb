class Api::V1::DeleteDeviceController < ApiController
    
    
    def create
        device =  @user.devices.find_by_uuid!(params[:uuid])
           
        render json: {status: 200}
    end
    
end
