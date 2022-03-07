//add subject to session
addTimeBlock(){                    
    axios.post('/session/{{id}}/', {
               action :"addTimeBlock" ,                                                                                                                                                                
        })
        .then(function (response) {    
            
            app.$data.session.parameterset = response.data.parameterset;        
            app.$data.session.session_days = response.data.session_days;                                   
        })
        .catch(function (error) {
            console.log(error);
        });                        
},

//add subject to session
removeTimeBlock(){                   
    axios.post('/session/{{id}}/', {
               action :"removeTimeBlock" ,                                                                                                                                                                
        })
        .then(function (response) {    
            
            app.$data.session.parameterset = response.data.parameterset;   
            app.$data.session.session_days = response.data.session_days;                                      
        })
        .catch(function (error) {
            console.log(error);
        });                        
},

//add subject to session
updateTimeBlock(){                    
    app.$data.cancelModal=true;

    axios.post('/session/{{id}}/', {
               action :"updateTimeBlock" ,      
               formData : $("#editTimeBlockForm").serializeArray(),  
               id : app.$data.current_time_block.id,                                                                                                                                                        
        })
        .then(function (response) {     
            status=response.data.status;                               

            app.clearMainFormErrors();

            if(status=="success")
            {
                app.$data.cancelModal=false;
                app.$data.session.parameterset = response.data.parameterset;    
                app.$data.session.session_days = response.data.session_days;   
                $('#editSessionParametersetTimeBlockModal').modal('toggle');      
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

//show edit parameters modal
showEditTimeBlock(index){
    app.clearMainFormErrors();

    app.$data.timeBlockBeforeEdit = Object.assign({}, app.$data.session.parameterset.time_blocks[index]);
    app.$data.current_time_block_index = index

    time_block = app.$data.session.parameterset.time_blocks[index];

    app.$data.current_time_block = time_block;
    
    app.$data.cancelModal=true;

    $('#editSessionParametersetTimeBlockModal').modal('show');                   
},

//fire when edit experiment model hides, cancel action if nessicary
hideEditTimeBlock(){
    if(app.$data.cancelModal)
    {
        index = app.$data.current_time_block_index;

        if(index != -1)
        {
            Object.assign(app.session.parameterset.time_blocks[index], app.$data.timeBlockBeforeEdit);
            app.$data.timeBlockBeforeEdit=null;
        }
    }
},

//add pay level
addPayLevel(){
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
removePayLevel(id){
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

//show edit parameters modal
showEditPaylevel:function(index){
    app.clearMainFormErrors();

    app.$data.paylevelBeforeEdit = Object.assign({}, app.$data.session.parameterset.pay_levels[index]);
    app.$data.current_paylevel_index = index

    paylevel = app.$data.session.parameterset.pay_levels[index];

    app.$data.current_paylevel = paylevel;
    
    app.$data.cancelModal=true;

    $('#editSessionParametersPaylevelModal').modal('show');                   
},

//fire when edit experiment model hides, cancel action if nessicary
hideEditPaylevel:function(){
    if(app.$data.cancelModal)
    {
        index = app.$data.current_paylevel_index;

        if(index != -1)
        {
            Object.assign(app.session.parameterset.pay_levels[index], app.$data.paylevelBeforeEdit);
            app.$data.paylevelBeforeEdit=null;
        }
    }
},

//update pay level
updatePaylevel(){
    app.$data.cancelModal=true;

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
                app.$data.cancelModal=false;
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

//download parameter set
downloadParameterset(){
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

//fire when show upload parameters
showUploadParameters:function(upload_mode){
    app.$data.upload_mode = upload_mode;
    app.$data.uploadParametersetMessaage = "";
    $('#parameterSetModal').modal('show');
},

//fire when upload parameters modal closes
hideUploadParameters:function(){
},

//upload parameter set
uploadParameterset(){  

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

//handle file upload inputbox
handleFileUpload:function(){
    app.$data.upload_file = this.$refs.file.files[0];
    //$('parameterFileUpload').val("");
    app.$data.upload_file_name = app.$data.upload_file.name;

},

//show edit parameters modal
showImportParameters:function(){

    $('#importParametersModal').modal('show');                   
},

//fire when edit experiment model hides, cancel action if nessicary
hideImportParameters:function(){
    if(app.$data.cancelModal)
    {

    }
},

//import parameters from another session
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