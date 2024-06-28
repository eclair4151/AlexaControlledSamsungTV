class Api::V1::AuthTokenController < ApiController
    skip_before_action :authenticate_user

    def create
        render json: {access_token: params[:code], token_type: 'Bearer'}
    end
end
