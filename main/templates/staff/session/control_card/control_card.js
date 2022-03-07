//activate session and fill session days
startSession(){
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

resetSession(){
    if(!confirm("Rest Session?  All data will be lost."))
    {                        
        return;
    }

    app.$data.resetSessionButtonText = '<i class="fas fa-spinner fa-spin"></i>';
    axios.post('/session/{{id}}/', {
               action :"resetSession" ,                                                                                                                                                               
        })
        .then(function (response) {     
            app.updateSession(response);      
            app.updateSubjects(response);    
            app.graph_parameters = response.data.graph_parameters;
            app.$data.resetSessionButtonText = 'Reset Session <i class="fas fa-retweet"></i>';                          
        })
        .catch(function (error) {
            console.log(error);
        }); 
},

//show cancel session
showCancelSession(){
            
    $('#sendCancelationsModalCenter').modal('show');                   
},

//hide cancel session
hideCancelSession(){
    app.$data.emailResultCancelation="";
},

//send cancelations
sendCancelations(){
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
                if(response.data.result.error_message != "")
                    app.$data.emailResultCancelation = "Error: " + response.data.result.error_message;
                else
                    app.$data.emailResultCancelation = response.data.result.mail_count + " email(s) were sent.";                                     
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

//for testing, back fill session days.
backFillSessionsDays(){        
    if(!confirm("Backfill session data?  For testing only."))
    {                        
        return;
    }

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

//send invitations
sendInvitations(){

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
                        if(response.data.result.error_message != "")
                            app.$data.emailResult = "Error: " + response.data.result.error_message;
                        else
                            app.$data.emailResult = response.data.result.mail_count + " email(s) were sent.";                                     
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

//download data
downloadData(){                    
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
downloadEarnings(){
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

