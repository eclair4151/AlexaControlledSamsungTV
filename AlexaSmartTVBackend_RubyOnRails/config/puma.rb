#daemonize true

app_dir = File.expand_path("../..", __FILE__)
shared_dir = "#{app_dir}/shared"
bind "unix://#{shared_dir}/sockets/puma.sock"

pidfile 'tmp/pids/puma.pid'
state_path 'tmp/pids/puma.state'

stdout_redirect "#{shared_dir}/log/puma.stdout.log", "#{shared_dir}/log/puma.stderr.log", true


# ssl_bind '0.0.0.0', '443', {
#   key: 'certificates/development-key.pem',
#   cert: 'certificates/development-cert.pem'
# }

