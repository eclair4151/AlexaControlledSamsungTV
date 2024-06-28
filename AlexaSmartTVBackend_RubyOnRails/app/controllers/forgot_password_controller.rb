class ForgotPasswordController < ApplicationController
  skip_before_action :authenticate_user
  layout 'root'

  def index
  end

  def create
    user = User.find_by_email(params[:email])
    if user
      reset_password(user)
    end

    redirect_to '/forgot_password', :flash => { :message => "If this user exists, a reset email password has been sent." }
  end
  
  


  def reset_password(user)
    password = (0...15).map { ('a'..'z').to_a[rand(26)] }.join
    user.password = password
    user.save
    RestClient.post "https://api.sendgrid.com/v3/mail/send", {
        "personalizations": [
            {
                "to": [
                    {
                        "email": user.email
                    }
                ]
            }
        ],
        "from": {
            "email": "forgotpassword@alexasmarttv.dev"
        },
        "subject": "Alexa Smart TV password reset",
        "content": [
            {
                "type": "text/plain",
                "value": "Hello,\n\nWe have generated a temporary password for you. Please go to alexasmarttv.dev/profile and change it. \n\nTemporary Password: " + password
            }
        ]
    }.to_json, {content_type: :json, accept: :json, Authorization: 'Bearer [YOUR_SENDGRID_API_KEY]'}
  end
end