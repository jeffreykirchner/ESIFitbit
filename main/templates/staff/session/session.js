axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

var app = new Vue({

    delimiters: ['[[', ']]'],
    el: '#root',        
    data:{
        sessionParametersBeforeEdit:{},                     //store session before editing to restore if canceled
        current_paylevel:{id : "",
                           score : "",
                           value : ""},
        session:{title:"",                                  //session and parameter set values
                    start_date:"",
                    end_date:"",
                    started:false,
                    instruction_set:{id:0,title:""},
                    invitations_sent:false,
                    invitation_text:"",
                    invitation_text_subject:"",
                    cancelation_text:"",
                    cancelation_text_subject:"",
                    email_list:"",
                    current_period:"",
                    complete:false,
                    consent_required:true,
                    questionnaire1_required:true,
                    questionnaire2_required:true,
                    treatment:"",
                    parameterset:{id:"",
                                number_of_days:"",
                                number_of_players:"",

                                heart_activity_inital:"",
                                heart_parameter_1:"",
                                heart_parameter_2:"",
                                heart_parameter_3:"",

                                immune_activity_inital:"",
                                immune_parameter_1:"",
                                immune_parameter_2:"",
                                immune_parameter_3:"",

                                block_1_heart_pay:"",
                                block_2_heart_pay:"",
                                block_3_heart_pay:"",

                                block_1_immune_pay:"",
                                block_2_immune_pay:"",
                                block_3_immune_pay:"",

                                block_1_fixed_pay_per_day:"",
                                block_2_fixed_pay_per_day:"",
                                block_3_fixed_pay_per_day:"",

                                minimum_wrist_minutes:"",

                                block_1_day_count:"",
                                block_2_day_count:"",
                                block_3_day_count:"",

                                pay_levels:[],
                            }
                },
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
        last_refresh:"",
        auto_refresh:"Off",
        timeouts:[],
    },

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

        //delete the selected experiment
        deleteSubject:function(id){
            if(confirm("Delete Subject?"))
            {
                axios.post('/session/{{id}}/', {
                    action :"deleteSubject" ,
                    id:id,                                                                                                                             
                })
                .then(function (response) {   
                    app.updateSession(response);
                    app.updateSubjects(response);                                                                          
                })
                .catch(function (error) {
                    console.log(error);
                });                        
            }
        },

        //create new experient
        addSubject:function(){                    
            app.$data.addSubjectButtonText ='<i class="fas fa-spinner fa-spin"></i>';
            axios.post('/session/{{id}}/', {
                            action :"addSubject" ,                                                                                                                                                                
                        })
                        .then(function (response) {     
                            app.updateSubjects(response);    
                            app.updateSession(response);      
                            app.$data.addSubjectButtonText = 'Add Subject <i class="fas fa-plus"></i>';                                        
                        })
                        .catch(function (error) {
                            console.log(error);
                        });                        
        },

        //refresh subject table click
        refreshSubjectTableClick:function(){

            if(app.$data.auto_refresh == "Off")
            {
                app.$data.auto_refresh = "On";
                this.refreshSubjectTable()
            }
            else
            {
                app.$data.auto_refresh = "Off";

                for (var i = 0; i < app.$data.timeouts.length; i++) {
                    clearTimeout(app.$data.timeouts[i]);
                }

                app.$data.timeouts=[];

                app.$data.refreshSubjectTableButtonText = 'Auto Refresh: ' + app.$data.auto_refresh + ' <i class="fas fa-sync"></i>';
            }
        },

        //refresh subject table()
        refreshSubjectTable:function(){

            app.$data.refreshSubjectTableButtonText = 'Auto Refresh: ' + app.$data.auto_refresh + ' <i class="fas fa-sync fa-spin"></i>';

            axios.post('/session/{{id}}/', {
                            action :"refreshSubjectTable" ,                                                                                                                                                                
                        })
                        .then(function (response) {     
                            app.updateSubjects(response);     
                            app.$data.refreshSubjectTableButtonText = 'Auto Refresh: ' + app.$data.auto_refresh + ' <i class="fas fa-sync"></i>';

                            if(app.$data.auto_refresh=="On")
                            {
                                app.$data.timeouts.push(setTimeout(app.refreshSubjectTable, 10000));            
                            }                            
                        })
                        .catch(function (error) {
                            console.log(error);
                        });
        },

        //update session parameters
        updateParameters:function(){                    
            app.$data.cancelModal=false;

            axios.post('/session/{{id}}/', {
                            action :"updateParameters" ,      
                            formData : $("#parametersetForm").serializeArray(),                                                                                                                                                          
                        })
                        .then(function (response) {     
                            status=response.data.status;                               

                            app.clearMainFormErrors();

                            if(status=="success")
                            {
                                app.updateSession(response);       
                                $('#editSessionParametersModal').modal('toggle');    
                            } 
                            else
                            {
                                app.$data.cancelModal=true;                           
                                app.displayErrors(response.data.errors);
                            }                                   
                        })
                        .catch(function (error) {
                            console.log(error);
                        });                        
        },

        //update session parameters
        updateSessionSettings:function(){                    
            app.$data.cancelModal=false;

            axios.post('/session/{{id}}/', {
                            action :"updateSession" ,      
                            formData : $("#sessionForm").serializeArray(),                                                                                                                                                          
                        })
                        .then(function (response) {     
                            status=response.data.status;                               

                            app.clearMainFormErrors();

                            if(status=="success")
                            {
                                app.updateSession(response);       
                                $('#editSessionModal').modal('toggle');    
                            } 
                            else
                            {
                                app.$data.cancelModal=true;                           
                                app.displayErrors(response.data.errors);
                            }                                   
                        })
                        .catch(function (error) {
                            console.log(error);
                        });                        
        },

        //for testing, back fill session days.
        backFillSessionsDays:function(){                    
            app.$data.backFillButtonText = '<i class="fas fa-spinner fa-spin"></i>';
            axios.post('/session/{{id}}/', {
                            action :"backFillSessionDays"                                                                                                                                                          
                        })
                        .then(function (response) {     
                            app.updateSession(response);   
                            app.updateSubjects(response);  

                            app.$data.backFillButtonText = 'Back Fill Data For Testing';                                    
                        })
                        .catch(function (error) {
                            console.log(error);
                        });                        
        },

        //activate session and fill session days
        startSession:function(){
            app.$data.startSessionButtonText = '<i class="fas fa-spinner fa-spin"></i>';
            axios.post('/session/{{id}}/', {
                            action :"startSession" ,                                                                                                                                                               
                        })
                        .then(function (response) {     
                            app.updateSession(response);      
                            app.$data.startSessionButtonText = 'Start Session <i class="far fa-play-circle"></i>';                          
                        })
                        .catch(function (error) {
                            console.log(error);
                        }); 
        },

        //send invitations
        sendInvitations:function(){

            if(app.$data.session.invitation_text_subject == "")
            {
                alert("Message has no subject.");
                return;
            }

            if(app.$data.session.invitation_text == "")
            {
                alert("Message is empty.");
                return;
            }

            app.$data.invitationButtonText = '<i class="fas fa-spinner fa-spin"></i>';
            axios.post('/session/{{id}}/', {
                            action :"sendInvitations" ,  
                            invitation_text_subject:app.$data.session.invitation_text_subject, 
                            invitation_text:app.$data.session.invitation_text,                                                                                                                                                            
                        })
                        .then(function (response) {     
                            app.updateSession(response);      
                            app.$data.invitationButtonText = 'Send Invitations <i class="far fa-envelope"></i>';   

                            if( response.data.success)
                            {
                                if(response.data.result.errorMessage != "")
                                    app.$data.emailResult = "Error: " + response.data.result.errorMessage;
                                else
                                    app.$data.emailResult = response.data.result.mailCount + " email(s) were sent.";                                     
                            }
                            else
                            {
                                app.$data.emailResult =response.data.result;
                            }
                                                    
                        })
                        .catch(function (error) {
                            console.log(error);
                        }); 
        },

        //get list of valid subjects to copy
        getSubjectsAvailableToCopy:function(){                    
            app.subjectsAvailableToCopyWorking = true;
            axios.post('/session/{{id}}/', {
                    action :"getSubjectsAvailableToCopy" ,                                                                                                                                                                
                })
                .then(function (response) {     
                    app.$data.subjectsAvailableToCopy = response.data.subjectsAvailableToCopy;           
                    app.subjectsAvailableToCopyWorking = false;                    
                })
                .catch(function (error) {
                    console.log(error);
                });                        
        },
        
        //copy subject
        sendCopySubject:function(id){                    
            app.subjectsAvailableToCopyWorking = true;
            axios.post('/session/{{id}}/', {
                    action : "sendCopySubject",
                    subject_id : id,                                                                                                                                                                
                })
                .then(function (response) {     
                    app.$data.subjectsAvailableToCopy = response.data.subjectsAvailableToCopy;          
                    app.updateSubjects(response); 
                    app.subjectsAvailableToCopyWorking = false;                    
                })
                .catch(function (error) {
                    console.log(error);
                });                        
        },

        //send cancelations
        sendCancelations:function(){
            if(!confirm("Cancel Session?"))
            {                        
                return;
            }

            if(app.$data.session.cancelation_text_subject == "")
            {
                alert("Message has no subject.");
                return;
            }

            if(app.$data.session.cancelation_text == "")
            {
                alert("Message is empty.");
                return;
            }

            app.$data.cancelationButtonText = '<i class="fas fa-spinner fa-spin"></i>';
            axios.post('/session/{{id}}/', {
                            action :"sendCancelations" ,  
                            cancelation_text_subject:app.$data.session.cancelation_text_subject, 
                            cancelation_text:app.$data.session.cancelation_text,                                                                                                                                                            
                        })
                        .then(function (response) {     
                            app.updateSession(response);      
                            app.$data.cancelationButtonText = 'Cancel Session <i class="fas fa-ban"></i>';   

                            if( response.data.success)
                            {
                                if(response.data.result.errorMessage != "")
                                    app.$data.emailResultCancelation = "Error: " + response.data.result.errorMessage;
                                else
                                    app.$data.emailResultCancelation = response.data.result.mailCount + " email(s) were sent.";                                     
                            }
                            else
                            {
                                app.$data.emailResultCancelation = response.data.result;
                            }
                                                
                        })
                        .catch(function (error) {
                            console.log(error);
                        }); 
            },

        //add pay level
        addPayLevel:function(){
            axios.post('/session/{{id}}/', {
                action :"addPayLevel" ,                                                                                                                                                           
            })
            .then(function (response) {     
                app.$data.session.parameterset = response.data.parameterset;                                         
            })
            .catch(function (error) {
                console.log(error);
            });
     
        },

        //remove pay level
        removePayLevel:function(id){
            axios.post('/session/{{id}}/', {
                action :"removePayLevel" ,  
                id : id,                                                                                                                                                         
            })
            .then(function (response) {     
                app.$data.session.parameterset = response.data.parameterset;                                         
            })
            .catch(function (error) {
                console.log(error);
            }); 
        },

        updatePaylevel:function(){
            axios.post('/session/{{id}}/', {
                action :"updatePaylevel" ,      
                formData : $("#parametersetLevelsForm").serializeArray(),  
                id : app.$data.current_paylevel.id,                                                                                                                                                        
            })
            .then(function (response) {     
                status=response.data.status;                               

                app.clearMainFormErrors();

                if(status=="success")
                {
                    app.$data.session.parameterset = response.data.parameterset;       
                    $('#editSessionParametersPaylevelModal').modal('toggle');    
                } 
                else
                {                       
                    app.displayErrors(response.data.errors);
                }                                   
            })
            .catch(function (error) {
                console.log(error);
            });
        },

        //show fitbit connection status for each subject
        showFitbitStatus:function(){                    
            app.$data.showFitbitStatusButtonText = '<i class="fas fa-spinner fa-spin"></i>';
            axios.post('/session/{{id}}/', {
                            action :"showFitbitStatus" ,                                                                                                                                                               
                        })
                        .then(function (response) {     
                            app.updateSubjects(response);      
                            app.$data.showFitbitStatusButtonText = 'Check fitbit <i class="far fa-check-circle"></i>';                          
                        })
                        .catch(function (error) {
                            console.log(error);
                        });                        
        },

        //copy subject link to clipboard
        copySubjectLinkToClipboard:function(text){

                // Create a dummy input to copy the string array inside it
            var dummy = document.createElement("input");

            // Add it to the document
            document.body.appendChild(dummy);

            // Set its ID
            dummy.setAttribute("id", "dummy_id");

            // Output the array into it
            document.getElementById("dummy_id").value=text;

            // Select it
            dummy.select();
            dummy.setSelectionRange(0, 99999); /*For mobile devices*/

            // Copy its contents
            document.execCommand("copy");

            // Remove it as its not needed anymore
            document.body.removeChild(dummy);

            /* Copy the text inside the text field */
            document.execCommand("copy");
        },

        //update subject parameters
        updateSubjectSettings:function(){                    
            app.$data.cancelModal=false;
            
            axios.post('/session/{{id}}/', {
                            action :"updateSubject" ,
                            ss_id : app.$data.currentSubject.id,      
                            formData : $("#subjectForm").serializeArray(),                                                                                                                                                          
                        })
                        .then(function (response) {     
                            status=response.data.status;                               

                            app.clearMainFormErrors();

                            if(status=="success")
                            {
                                app.updateSubjects(response);       
                                $('#editSubjectModal').modal('toggle');    
                            } 
                            else
                            {
                                app.$data.cancelModal=true;                           
                                app.displayErrors(response.data.errors);
                            }                                   
                        })
                        .catch(function (error) {
                            console.log(error);
                        });                        
        },

        //download data
        downloadData:function(){                    
            app.$data.downloadDataButtonText = '<i class="fas fa-spinner fa-spin"></i>';
            axios.post('/session/{{id}}/', {
                            action :"downloadData" ,                                                                                                                                                                                              
                        })
                        .then(function (response) {     
                                                        
                            
                            console.log(response.data);

                            var downloadLink = document.createElement("a");
                            var blob = new Blob(["\ufeff", response.data]);
                            var url = URL.createObjectURL(blob);
                            downloadLink.href = url;
                            downloadLink.download = "FitBit_Session_" + app.$data.session.id +"_Data.csv";

                            document.body.appendChild(downloadLink);
                            downloadLink.click();
                            document.body.removeChild(downloadLink);

                            app.$data.downloadDataButtonText ='Download Data <i class="fas fa-scroll fa-xs"></i>';
                                                            
                        })
                        .catch(function (error) {
                            console.log(error);
                        });                        
        },

        //download earnings
        downloadEarnings:function(){
            app.$data.downloadEarningsButtonText = '<i class="fas fa-spinner fa-spin"></i>';
            axios.post('/session/{{id}}/', {
                            action :"downloadEarnings",
                            date : app.$data.earningsDownloadDate,                                                                                                                                                                                              
                        })
                        .then(function (response) {    
                                                        
                            console.log(response.data);

                            var downloadLink = document.createElement("a");
                            var blob = new Blob(["\ufeff", response.data]);
                            var url = URL.createObjectURL(blob);
                            downloadLink.href = url;
                            downloadLink.download = "FitBit_Session_" + app.$data.session.id +"_Earnings_" + app.$data.earningsDownloadDate + ".csv";

                            document.body.appendChild(downloadLink);
                            downloadLink.click();
                            document.body.removeChild(downloadLink);

                            app.$data.downloadEarningsButtonText ='Download Earnings <i class="fas fa-cash-register"></i>';
                                                            
                        })
                        .catch(function (error) {
                            console.log(error);
                        });
        },

        //download parameter set
        downloadParameterset:function(){
            app.$data.downloadParametersetButtonText = '<i class="fas fa-spinner fa-spin"></i>';

            axios.post('/session/{{id}}/', {
                            action :"downloadParameterset",
                                                                                                                                                                                                
                        })
                        .then(function (response) {    
                                                        
                            console.log(response.data.parameterset);

                            var downloadLink = document.createElement("a");
                            var jsonse = JSON.stringify(response.data.parameterset);
                            var blob = new Blob([jsonse], {type: "application/json"});
                            var url = URL.createObjectURL(blob);
                            downloadLink.href = url;
                            downloadLink.download = "FitBit_Session_" + app.$data.session.id + "_Parameter_Set.json";

                            document.body.appendChild(downloadLink);
                            downloadLink.click();
                            document.body.removeChild(downloadLink);

                            app.$data.downloadParametersetButtonText ='Download <i class="fas fa-download"></i>';
                                                            
                        })
                        .catch(function (error) {
                            console.log(error);
                        });

        },

        uploadParameterset:function(){  

            let formData = new FormData();
            formData.append('file', app.$data.upload_file);

            axios.post('/session/{{id}}/', formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                            }
                        } 
                    )
                    .then(function (response) {     

                        app.$data.uploadParametersetMessaage = response.data.message;

                        app.updateSession(response);

                        app.$data.uploadParametersetButtonText= 'Upload <i class="fas fa-upload"></i>';

                    })
                    .catch(function (error) {
                        console.log(error);
                        app.$data.searching=false;
                    });                        
        },
        
        //upload a list of subjects from a csv file        
        uploadSubjects:function(){
            

            let formData = new FormData();
            formData.append('file', app.$data.upload_file);

            axios.post('/session/{{id}}/', formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                            }
                        } 
                    )
                    .then(function (response) {     

                        app.$data.uploadParametersetMessaage = response.data.message;
                        app.updateSubjects(response);

                        app.$data.uploadParametersetButtonText= 'Upload <i class="fas fa-upload"></i>';
                                                                        
                    })
                    .catch(function (error) {
                        console.log(error);
                        app.$data.searching=false;
                    });                        
        },

        //direct upload button click
        uploadAction:function(){
            if(app.$data.upload_file == null)
                return;

            app.$data.uploadParametersetMessaage = "";
            app.$data.uploadParametersetButtonText = '<i class="fas fa-spinner fa-spin"></i>';

            if(app.$data.upload_mode == "parameters")
            {
                this.uploadParameterset();
            }
            else
            {
                this.uploadSubjects();
            }

        },

        handleFileUpload:function(){
            app.$data.upload_file = this.$refs.file.files[0];
            //$('parameterFileUpload').val("");
            app.$data.upload_file_name = app.$data.upload_file.name;

            },

        //import parameters
        importParameters:function(){                   
            
            axios.post('/session/{{id}}/', {
                            action :"importParameters" ,     
                            formData : $("#parametersImportForm").serializeArray(),                                                                                                                                                          
                        })
                        .then(function (response) {     
                            app.updateSession(response);       
                            $('#importParametersModal').modal('toggle');                                  
                        })
                        .catch(function (error) {
                            console.log(error);
                        });                        
        },

        //show edit parameters modal
        showEditParameters:function(){
            app.clearMainFormErrors();
            app.$data.cancelModal=true;
            app.$data.sessionParametersBeforeEdit = Object.assign({}, app.$data.session.parameterset);
            $('#editSessionParametersModal').modal('show');                   
        },

        //fire when edit experiment model hides, cancel action if nessicary
        hideEditParameters:function(){
            if(app.$data.cancelModal)
            {
                Object.assign(app.$data.session.parameterset, app.$data.sessionParametersBeforeEdit);
                app.$data.sessionBeforeEdit=null;
            }
        },

        //show edit parameters modal
        showEditSession:function(){
            app.clearMainFormErrors();
            app.$data.cancelModal=true;
            app.$data.sessionBeforeEdit = Object.assign({}, app.$data.session);
            $('#editSessionModal').modal('show');                   
        },

        //fire when edit experiment model hides, cancel action if nessicary
        hideEditSession:function(){
            if(app.$data.cancelModal)
            {
                Object.assign(app.$data.session, app.$data.sessionBeforeEdit);
                app.$data.sessionBeforeEdit=null;
            }
        },

        //show edit parameters modal
        showEditSubject:function(s_id,index){
            app.clearMainFormErrors();
            app.$data.cancelModal=true;
            app.$data.currentSubjectIndex = index
            app.$data.subjectBeforeEdit = Object.assign({}, app.$data.session_subjects[index]);
            app.$data.currentSubject = app.$data.session_subjects[index];
            $('#editSubjectModal').modal('show');                   
        },

        //fire when edit experiment model hides, cancel action if nessicary
        hideEditSubject:function(){
            if(app.$data.cancelModal)
            {
                index = app.$data.currentSubjectIndex;

                if(index != -1)
                {
                    Object.assign(app.$data.session_subjects[index], app.$data.subjectBeforeEdit);
                    app.$data.subjectBeforeEdit=null;
                }
            }
        },

        //show edit parameters modal
        showEditPaylevel:function(index){
            app.clearMainFormErrors();

            paylevel = app.$data.session.parameterset.pay_levels[index];

            app.$data.current_paylevel = paylevel;
            
            $('#editSessionParametersPaylevelModal').modal('show');                   
        },

        //fire when edit experiment model hides, cancel action if nessicary
        hideEditPaylevel:function(){
            
        },

        //show send invitation
        showSendInvitations:function(){
            
            $('#sendMessageModalCenter').modal('show');                   
        },

        //hide send invitation
        hideSendInvitations:function(){
            app.$data.emailResult="";
        },

        //show cancel session
        showCancelSession:function(){
            
            $('#sendCancelationsModalCenter').modal('show');                   
        },

        //hide cancel session
        hideCancelSession:function(){
            app.$data.emailResultCancelation="";
        },
                    
        //show edit parameters modal
        showImportParameters:function(){

            $('#importParametersModal').modal('show');                   
        },

        //fire when edit experiment model hides, cancel action if nessicary
        hideImportParameters:function(){
            if(app.$data.cancelModal)
            {
                // index = currentSubjectIndex;

                // if(index != -1)
                // {
                //     Object.assign(app.$data.session_subjects[index], app.$data.subjectBeforeEdit);
                //     app.$data.subjectBeforeEdit=null;
                // }
            }
        },
    
        //fire when show upload parameters
        showUploadParameters:function(upload_mode){
            app.$data.upload_mode = upload_mode;
            app.$data.uploadParametersetMessaage = "";
            $('#parameterSetModal').modal('show');
        },

        hideUploadParameters:function(){
        },
                    
        //show edit parameters modal
        showCopySubject:function(){
            app.getSubjectsAvailableToCopy();
            $('#copySubjectModal').modal('show');                   
        },
        
        //hide cancel session
        hideCopySubject:function(){
           
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
        },       
        
        //graphs
        //change graph toggle state
        updateToogleState:function(toggleState){
            app.$data.toggleState = toggleState;
            Vue.nextTick(app.updateCanvases());    
        },

        //update canvas with current toggle state
        updateCanvases:function(){

            var el = $('#healthChart');
            el.attr('width', parseInt(el.css('width')))
            el.attr('height', parseInt(el.css('height')))
            
            periodCount = 0;
            ss = app.$data.session_subjects;

            if(ss.length == 0) return;   

            periodCount = ss[0].heart_minutes.length;                 
            if(periodCount == 0 ) return;

            gp=app.$data.graph_parameters;

            if(app.$data.toggleState == "heart")
            {
                app.drawAxis("healthChart",0,gp.x_max_heart,2,
                                                0,periodCount,periodCount,
                                                "Zone Minutes","Period");

                for(var j=0;j<ss.length;j++)
                {
                    //console.log(j);
                    app.drawLine("healthChart",0,gp.x_max_heart,
                                            0,periodCount,
                                            ss[j].heart_minutes,1,ss[j].display_color);
                }
            
            
            }
            else
            {
                app.drawAxis("healthChart",0,gp.x_max_immune,2,
                                            0,periodCount,periodCount,
                                            "Hours Asleep","Period");    

                                            for(var j=0;j<ss.length;j++)
                {
                    //console.log(j);
                    app.drawLine("healthChart",0,gp.x_max_immune,
                                            0,periodCount,
                                            ss[j].immune_minutes,1,ss[j].display_color);
                }  
            }          
        },

        drawAxis: function (chartID,yMin,yMax,yTickCount,xMin,xMax,xTickCount,yLabel,xLabel){
    
            if(document.getElementById(chartID) == null)
            {
                return;
            }

            var canvas = document.getElementById(chartID),
                ctx = canvas.getContext('2d');    

            var xScale = xMax-xMin;
            var yScale = yMax-yMin;

            var w = ctx.canvas.width;
            var h = ctx.canvas.height;
            var marginY=45;
            var marginX=40;
            var margin2=10;
            var tickLength=3;
            
            var xTickValue=xScale/parseFloat(xTickCount);
            var yTickValue=yScale/parseFloat(yTickCount);
        
            ctx.moveTo(0,0);

            //clear screen
            // ctx.fillStyle = "white";
            // ctx.fillRect(0,0,w,h);
            ctx.clearRect(0,0,w,h);
            ctx.strokeStyle="black";
            ctx.lineWidth=3;

            //axis
            ctx.beginPath();
            ctx.moveTo(marginY, margin2);
            ctx.lineTo(marginY, h-marginX);
            ctx.lineTo(w-margin2, h-marginX);
            ctx.lineWidth = 3;
            ctx.lineCap = "round";
            ctx.stroke();

            //y ticks
            ctx.beginPath();                                                               
            ctx.font="12px Georgia";
            ctx.fillStyle = "black";
            ctx.textAlign = "right";

            var tempY = h-marginX;     
            var tempYValue = yMin;

            for(var i=0;i<=yTickCount;i++)
            {                                       
                ctx.moveTo(marginY, tempY);                                   
                ctx.lineTo(marginY-5, tempY);
                ctx.fillText(tempYValue,marginY-8,tempY+4);

                tempY -= ((h-marginX-margin2)/ (yTickCount));
                tempYValue += yTickValue;
            }

            ctx.stroke();

            //x ticks
            ctx.beginPath();                                                               
            ctx.textAlign = "center";

            var tempX = marginY;
            var tempXValue=xMin;                                
            for(var i=0;i<=xTickCount;i++)
            {                                       
                ctx.moveTo(tempX, h-marginX);                                   
                ctx.lineTo(tempX,  h-marginX+5);
                ctx.fillText(Math.round(tempXValue).toString(),tempX,h-marginX+18);

                tempX += ((w-marginY-margin2)/ (xTickCount));
                tempXValue += xTickValue;
            }

            ctx.stroke();

            //labels
            ctx.textAlign = "center";
            ctx.fillStyle = "DimGray";
            ctx.font="bold 14px Georgia"; 

            ctx.save();
            ctx.translate(14, h/2);
            ctx.rotate(-Math.PI/2);                                                              
            ctx.fillText(yLabel,0,0);
            ctx.restore();

            ctx.fillText(xLabel,w/2,h-4);
            ctx.restore();                       
        },

        drawLine: function (chartID,yMin,yMax,xMin,xMax,dataSet,markerWidth,markerColor){

            if(document.getElementById(chartID) == null)
            {
                return;
            }

            if(app.$data.session.current_period=="---"  && !app.$data.session.complete)
            {
                return;
            }

            var canvas = document.getElementById(chartID),
                ctx = canvas.getContext('2d');           

            var w =  ctx.canvas.width;
            var h = ctx.canvas.height;
            var marginY=45;
            var marginX=40;
            var margin2=10;
            var tickLength=3;

            ctx.save();

            ctx.strokeStyle = markerColor;
            ctx.fillStyle = markerColor;
            ctx.lineWidth = markerWidth;

            ctx.translate(marginY, h-marginX);
            ctx.moveTo(0, 0);

            
            for(i=0;i<dataSet.length;i++)
            {
                //stop line at current period
                if (app.$data.session.current_period !="---")
                {
                    if(i >= app.$data.session.current_period-1)
                    {
                        break;
                    }
                }

                x = app.convertToX(i+1,xMax,xMin,w-marginY-margin2,markerWidth);
                y = app.convertToY(dataSet[i],yMax,yMin,h-marginX-margin2,markerWidth);

                //ignore gaps
                if(i>0)
                {
                    if(dataSet[i-1] >= 0 && dataSet[i] >= 0)
                    {
                        x1 = app.convertToX(i,xMax,xMin,w-marginY-margin2,markerWidth);
                        y1 = app.convertToY(dataSet[i-1],yMax,yMin,h-marginX-margin2,markerWidth);

                        ctx.beginPath();
                        ctx.moveTo(x1,y1);
                        ctx.lineTo(x,y);
                        ctx.stroke();
                    }
                    
                }
                        
                if(dataSet[i] >= 0 )
                {
                    ctx.beginPath();
                    ctx.arc(x,y,3,0,2*Math.PI);
                    ctx.fill();   
                }                    

            }    

            
                
            ctx.restore();                                         
        },

        convertToX:function(tempValue,maxValue,minValue,tempWidth, markerWidth){
            tempT = tempWidth / (maxValue-minValue);

            tempValue-=minValue;

            if(tempValue>maxValue) tempValue=maxValue;

            return (tempT * tempValue - markerWidth/2);
        },

        convertToY:function(tempValue,maxValue,minValue,tempHeight, markerHeight){
            tempT = tempHeight / (maxValue-minValue);

            if(tempValue > maxValue) tempValue=maxValue;
            if(tempValue < minValue) tempValue=minValue;

            tempValue-=minValue;

            if(tempValue>maxValue) tempValue=maxValue;

            return(-1 * tempT * tempValue - markerHeight/2)
        },
    },

    mounted: function(){
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
    },
});