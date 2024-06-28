class ProfileController < ApplicationController
  def index
    @email = @user.email
  end
  
  
  
  def create
    if params[:email]
      if !isEmail(params[:email])
        redirect_to '/profile', :flash => { :error => "Invalid Email" }
      else
        @user.email = params[:email]
        @user.save
        redirect_to '/profile', :flash => { :message => "Email Updated" }
      end
    end
    
    if params[:password] and params[:cpassword]
      if params[:password] != params[:cpassword]
        redirect_to '/profile', :flash => { :error => "Passwords do not match" }
      else
         @user.password = params[:password]
         @user.save
         redirect_to '/profile', :flash => { :message => "Password Updated" }
      end
    end
    
  end
  
  
  
  def isEmail(str)
    return str.match(/\A([\w+\-].?)+@[a-z\d\-]+(\.[a-z]+)*\.[a-z]+\z/i)
  end
  
  
end
