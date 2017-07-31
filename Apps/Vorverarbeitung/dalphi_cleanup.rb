# http://192.168.178.77:3000
require 'awesome_print'

ap 'login...'
authentification = DalphiProfiler::Authentification.new email: 'robert@implisense.com',
                                                        password: 'Versuchsleiter'
authentification.login_admin # logs in an administrator with the specified credentials

for vp_index in 32..48 do
  # vp_index = 17 # debug

  number = vp_index.to_s
  number = "0#{vp_index}" if vp_index < 10
  vp_id = "VP#{number}"
  vp_email = "vp#{number}@study.com"
  project_id = "Studie für #{vp_id}"

  ap "remove annotator '#{vp_id}'..."
  annotator = DalphiProfiler::Annotator.new name: vp_id,
                                            email: vp_email
  # annotator.create # creates an annotator with the specified name and credentials
  annotator.destroy # destroys an annotator identified by the name
  # annotator.assign_to_project project_title: project_id # assignes the annotator identified by the name and email to the project identified by its title
  # annotator.unassign_from_project project_title: 'news-data' # unassignes the annotator identified by its name from the project identified by its title
end

authentification.logout_admin # logs out any logged in administrator
