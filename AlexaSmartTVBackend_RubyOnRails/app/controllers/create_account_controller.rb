class CreateAccountController < ApplicationController
  skip_before_action :authenticate_user
  layout 'root'

  def index
  end

  def create
    if User.find_by_email(params[:email])
      redirect_to '/create_account', :flash => { :error => "Email already in use" }
    elsif !isEmail(params[:email])
      redirect_to '/create_account', :flash => { :error => "Invalid Email" }
    elsif params[:password] != params[:c_password]
      redirect_to '/create_account', :flash => { :error => "Passwords do not match" }
    else
        user = User.create!(email:  params[:email].downcase, first_name:  params[:first_name], last_name:  params[:last_name], password:  params[:password])
        jwt_payload = {user_id: user.id}
        token = JWT.encode jwt_payload, Rails.application.secrets[:jwt_key], 'HS256'
        cookies[:jwt] = { :value => token, :expires => 3.months.from_now }
        redirect_to '/'
    end
  end
  
  
  
  def isEmail(str)
    return str.match(/\A([\w+\-].?)+@[a-z\d\-]+(\.[a-z]+)*\.[a-z]+\z/i)
  end

end
