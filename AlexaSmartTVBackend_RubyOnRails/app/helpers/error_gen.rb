class ErrorGen
  def self.create_error(status, message)
     {error:{status:status, message: message}}
  end
end