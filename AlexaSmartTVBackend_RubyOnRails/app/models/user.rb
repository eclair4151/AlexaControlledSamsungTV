require 'csv'
class User < ActiveRecord::Base
  has_many :devices
  has_secure_password
end