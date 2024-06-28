class Api::V1::PingController < ApiController

    def create
        device =  @user.devices.find_by_uuid!(params[:uuid])
        device.touch(:last_pinged)
        device.deleted = false
        device.save
        render json: {status: 200}
    end
       
end
