//delete the selected experiment
deleteSubject(id){
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

//add subject to session
addSubject(){                    
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
refreshSubjectTableClick(){

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

//refresh subject table
refreshSubjectTable(){

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

//get list of valid subjects to copy
getSubjectsAvailableToCopy(){                    
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
sendCopySubject(id){                    
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

//show edit parameters modal
showCopySubject:function(){
    app.getSubjectsAvailableToCopy();
    $('#copySubjectModal').modal('show');                   
},

//hide cancel session
hideCopySubject:function(){
   
},

//show fitbit connection status for each subject
showFitbitStatus(){                    
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
copySubjectLinkToClipboard(text){

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

//update subject parameters
updateSubjectSettings(){                    
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