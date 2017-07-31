# http://192.168.178.77:3000
require 'awesome_print'

VP_PASSWORD = "Versuchsperson"

def generate_raw_datum_file_names(number)
  [
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/a_preannotated_subject_corpus_document.json",
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/b_preannotated_subject_corpus_document.json",
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/c_preannotated_subject_corpus_document.json",
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/d_preannotated_subject_corpus_document.json",
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/e_preannotated_subject_corpus_document.json",
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/f_preannotated_subject_corpus_document.json",
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/g_preannotated_subject_corpus_document.json",
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/h_preannotated_subject_corpus_document.json",
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/i_preannotated_subject_corpus_document.json",
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/j_preannotated_subject_corpus_document.json",
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/k_preannotated_subject_corpus_document.json",
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/l_preannotated_subject_corpus_document.json",
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/m_preannotated_subject_corpus_document.json",
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/n_preannotated_subject_corpus_document.json",
    "/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/VP#{number}/o_preannotated_subject_corpus_document.json"
  ]
end

ap 'login...'
authentification = DalphiProfiler::Authentification.new email: 'robert@implisense.com',
                                                        password: 'Versuchsleiter'
authentification.login_admin # logs in an administrator with the specified credentials

for vp_index in 50..66 do
  # vp_index = 17 # debug

  number = vp_index.to_s
  number = "0#{vp_index}" if vp_index < 10
  vp_id = "VP#{number}"
  vp_email = "vp#{number}@study.com"
  project_id = "Studie für #{vp_id}"

  # ap "create a new project '#{project_id}'..."
  # project = DalphiProfiler::Project.new title: project_id,
  #                                       description: 'Klicke hier um die Studie zu beginnen',
  #                                       iterate_service: 'Research Study Iterator',
  #                                       merge_service: 'Research Study Merger',
  #                                       interfaces: {
  #                                         'ner_complete' => 'NER Complete',
  #                                         'questionnaire' => 'Questionnaire'
  #                                       }
  # project.create # creates a project with the specified preferences
  # # project.destroy # destroys a project with the specified title
  #
  # ap "create new raw data..."
  # raw_datum = DalphiProfiler::RawDatum.new project_title: project_id,
  #                                          files: generate_raw_datum_file_names(number)
  # raw_datum.create # creates a raw datum with the given file for the project with the specified project title
  # # raw_datum.destroy_all # destroys all raw data associated to the project with the given title

  # ap "generate annotation documents..."
  # annotation_document = DalphiProfiler::AnnotationDocument.new project_title: project_id
  # annotation_document.create # creates an annotation document for the project with the specified project title
  # # annotation_document.destroy_all # destroys all annotation documents associated to the project with the given title

  ap "create a new annotator '#{vp_id}'..."
  annotator = DalphiProfiler::Annotator.new name: vp_id,
                                            email: vp_email,
                                            password: VP_PASSWORD
  # annotator.create # creates an annotator with the specified name and credentials
  # annotator.destroy # destroys an annotator identified by the name
  annotator.assign_to_project project_title: project_id # assignes the annotator identified by the name and email to the project identified by its title
  # annotator.unassign_from_project project_title: 'news-data' # unassignes the annotator identified by its name from the project identified by its title
end

authentification.logout_admin # logs out any logged in administrator
