payMe:function(){

    if(!app.$data.viewed_heart)
    {
        alert("Please view Heart Health tab before payment.")
        return;
    }

    if(!app.$data.viewed_immune)
    {
        alert("Please view the Sleep Health tab before payment.")
        return;
    }

    if(!app.$data.viewed_group)
    {
        alert("Please view the Group tab before payment.")
        return;
    }

    app.$data.payMeButtonText = '<i class="fas fa-spinner fa-spin"></i>';

    axios.post('/subjectHome/{{id}}/', {
                    action :"payMe" ,                                                                                                                                                                
                })
                .then(function (response) {     
                    app.$data.session_day_subject_actvity = response.data.session_day_subject_actvity;  
                    app.$data.session_complete = response.data.session_complete;

                    app.$data.payMeButtonText = 'Pay Me <i class="fab fa-paypal fa-lg"></i>';     

                    if(response.data.status == "fail")
                        app.$data.paymentError=true;
                    else
                        app.$data.paymentError=false;    

                })
                .catch(function (error) {
                    console.log(error);
                });
},