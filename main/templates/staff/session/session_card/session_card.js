//show edit parameters modal
showEditSession(){
    app.clearMainFormErrors();
    app.$data.cancelModal=true;
    app.$data.sessionBeforeEdit = Object.assign({}, app.$data.session);
    $('#editSessionModal').modal('show');                   
},

//fire when edit experiment model hides, cancel action if nessicary
hideEditSession(){
    if(app.$data.cancelModal)
    {
        Object.assign(app.$data.session, app.$data.sessionBeforeEdit);
        app.$data.sessionBeforeEdit=null;
    }
},

//update session parameters
updateSessionSettings(){                    
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

//show edit parameters modal
showViewSessionDayModal(){

    $('#viewSessionDayModal').modal('show');                   
},

//fire when edit experiment model hides, cancel action if nessicary
hideViewSessionDayModal(){
    if(app.$data.cancelModal)
    {
       
    }
},

//show edit session day modal
showEditSessionDayModal(index){
    app.clearMainFormErrors();

    app.$data.sessionDayBeforeEdit = Object.assign({}, app.$data.session.session_days[index]);
    app.$data.current_session_day_index = index

    session_day = app.$data.session.session_days[index];

    app.$data.current_session_day = session_day;
    
    app.$data.cancelModal=true;

    $('#editSessionDayModal').modal('show');                   
},

//fire when hide edit session day model
hideEditSessionDayModal(){
    if(app.$data.cancelModal)
    {
        index = app.$data.current_session_day_index;

        if(index != -1)
        {
            Object.assign(app.$data.session.session_days[index], app.$data.sessionDayBeforeEdit);
            app.$data.sessionDayBeforeEdit=null;
        }
    }
},

updateSessionDay(){                    
    app.$data.cancelModal=true;

    axios.post('/session/{{id}}/', {
               action :"updateSessionDay" ,      
               formData : $("#sessionDayForm").serializeArray(),  
               id : app.$data.current_session_day.id,                                                                                                                                                        
        })
        .then(function (response) {     
            status=response.data.status;                               

            app.clearMainFormErrors();

            if(status=="success")
            {
                app.$data.cancelModal=false;
                app.$data.session.session_days = response.data.session_days;       
                $('#editSessionDayModal').modal('toggle');      
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