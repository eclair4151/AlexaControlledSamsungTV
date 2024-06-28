class LoginController < ApplicationController
  skip_before_action :authenticate_user
  layout 'root'
  
  
  def index
   
  end


  def create
    user = User.find_by_email(params[:email].strip.downcase)
    if user!= nil and user.authenticate(params[:password])
      jwt_payload = {user_id: user.id}
      token = JWT.encode jwt_payload, Rails.application.secrets[:jwt_key], 'HS256'
      cookies[:jwt] = { :value => token, :expires => 3.months.from_now }
      redirect_to '/'
    else
      redirect_to '/login', :flash => { :error => "Incorrect Username or Password" }
    end
  end

end