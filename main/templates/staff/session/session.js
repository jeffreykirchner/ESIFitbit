axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

var app = Vue.createApp({

    delimiters: ['[[', ']]'],
      
    data() {return {
        sessionParametersBeforeEdit:{},                     //store session before editing to restore if canceled
        current_paylevel:{{pay_level_json|safe}},
        current_time_block:{{time_block_json|safe}},
        session:{{session_json|safe}},
        current_session_day:{{current_session_day|safe}},
        session_subjects:[],              //list of subjects in this session 
        cancelModal:false,                //if modal is canceled reload old values
        currentSubject:{},                //current subject being edited
        currentSubjectIndex:-1,           //index of current subject being edited
        subjectsAvailableToCopy:[],       //list of all session that can be copied from another session
        subjectsAvailableToCopyWorking:false,  //working on adding copying a subject
        addSubjectButtonText:'Add Subject <i class="fas fa-plus"></i>',
        showFitbitStatusButtonText:'Check fitbit <i class="far fa-check-circle"></i>',
        backFillButtonText:'Back Fill Data For Testing',
        startSessionButtonText: 'Start Session <i class="far fa-play-circle"></i>',
        resetSessionButtonText: 'Reset Session <i class="fas fa-retweet"></i>',
        invitationButtonText: 'Send Invitations <i class="far fa-envelope"></i>',
        cancelationButtonText: 'Cancel Session <i class="fas fa-ban"></i>',
        downloadDataButtonText:'Download Data <i class="fas fa-scroll fa-xs"></i>',
        downloadEarningsButtonText:'Download Earnings <i class="fas fa-cash-register"></i>',
        downloadParametersetButtonText:'Download <i class="fas fa-download"></i>',
        uploadParametersetButtonText:'Upload  <i class="fas fa-upload"></i>',
        uploadParametersetMessaage:'',
        upload_file: null,
        upload_file_name:'Choose File',
        upload_mode:'',         //parameters or subject
        refreshSubjectTableButtonText:'Auto Refresh: Off <i class="fas fa-sync fa-spin"></i>',
        emailResult:'',
        emailResultCancelation:'',
        helpTitle:"Session Help",
        helpText:`{{help_text|safe}}`,
        toggleState:"heart",
        graph_parameters:{},
        earningsDownloadDate:"{{yesterdays_date}}",
        subject_form_ids:{{subject_form_ids|safe}},
        paylevel_form_ids:{{paylevel_form_ids|safe}},
        time_block_form_ids:{{time_block_form_ids|safe}},
        session_day_form_ids:{{session_day_form_ids|safe}},
        last_refresh:"",
        auto_refresh:"Off",
        timeouts:[],
    }},

    methods:{

        //create new experient
        getSession:function(){                    
            
            axios.post('/session/{{id}}/', {
                            action :"getSession" ,                                                                                                                                                                
                        })
                        .then(function (response) {     
                            app.updateSession(response);   
                            app.updateSubjects(response);    
                            app.graph_parameters = response.data.graph_parameters;
                            app.$data.refreshSubjectTableButtonText='Auto Refresh: ' + app.$data.auto_refresh + ' <i class="fas fa-sync"></i>';    
                            Vue.nextTick(app.updateCanvases());                               
                        })
                        .catch(function (error) {
                            console.log(error);
                        });                        
        },
                        
        //take update for the session parameters
        updateSession:function(response){
            app.$data.session = response.data.session;           
        },

        //take update the subject list
        updateSubjects:function(response){
            app.$data.session_subjects = response.data.session_subjects;      
            Vue.nextTick(app.updateCanvases());    
            
            app.$data.last_refresh = moment(new Date).local().format('MM/DD/YYYY hh:mm:ss a');                  
        },

        displayErrors:function(errors){
            for(var e in errors)
            {
                $("#id_" + e).attr("class","form-control is-invalid")
                var str='<span id=id_errors_'+ e +' class="text-danger">';
                
                for(var i in errors[e])
                {
                    str +=errors[e][i] + '<br>';
                }

                str+='</span>';
                $("#div_id_" + e).append(str); 

                var elmnt = document.getElementById("div_id_" + e);
                elmnt.scrollIntoView(); 

            }
        }, 

        clearMainFormErrors:function(){
            for(var item in app.$data.session.parameterset)
            {
                $("#id_" + item).attr("class","form-control");
                $("#id_errors_" + item).remove();
            }
            
            for(var item in app.$data.session)
            {
                $("#id_" + item).attr("class","form-control");
                $("#id_errors_" + item).remove();
            }

            s = app.$data.subject_form_ids;
            for(var i in s)
            {
                $("#id_" + s[i]).attr("class","form-control");
                $("#id_errors_" + s[i]).remove();
            }

            s = app.$data.paylevel_form_ids;
            for(var i in s)
            {
                $("#id_" + s[i]).attr("class","form-control");
                $("#id_errors_" + s[i]).remove();
            }

            s = app.time_block_form_ids;
            for(var i in s)
            {
                $("#id_" + s[i]).attr("class","form-control");
                $("#id_errors_" + s[i]).remove();
            }

            s = app.session_day_form_ids;
            for(var i in s)
            {
                $("#id_" + s[i]).attr("class","form-control");
                $("#id_errors_" + s[i]).remove();
            }
        },       
        
        {%include "staff/session/subjects_card/subjects_card.js"%}
        {%include "staff/session/session_card/session_card.js"%}
        {%include "staff/session/parameters_card/parameters_card.js"%}
        {%include "staff/session/control_card/control_card.js"%}
        {%include "staff/session/graph_card/graph_card.js"%}
    },

    mounted(){
        this.getSession();        
        $('#editSessionParametersModal').on("hidden.bs.modal", this.hideEditParameters);  
        $('#editSessionModal').on("hidden.bs.modal", this.hideEditSession);   
        $('#importParametersModal').on("hidden.bs.modal", this.hideImportParameters);
        $('#sendMessageModalCenter').on("hidden.bs.modal", this.hideSendInvitations); 
        $('#sendCancelationsModalCenter').on("hidden.bs.modal", this.hideCancelSession);  
        $('#editSubjectModal').on("hidden.bs.modal", this.hideEditSubject);  
        $('#hideUploadParameters').on("hidden.bs.modal", this.hideEditSubject); 
        $('#copySubjectModal').on("hidden.bs.modal", this.hideCopySubject); 
        $('#editSessionParametersPaylevelModal').on("hidden.bs.modal", this.hideEditPaylevel); 
        $('#editSessionParametersetTimeBlockModal').on("hidden.bs.modal", this.hideEditTimeBlock);
        $('#viewSessionDayModal').on("hidden.bs.modal", this.hideViewSessionDayModal);
        $('#editSessionDayModal').on("hidden.bs.modal", this.hideEditSessionDayModal);
    },
}).mount('#app');