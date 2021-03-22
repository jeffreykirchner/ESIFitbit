
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

var app = new Vue({

    delimiters: ['[[', ']]'],
    el: '#root',        
    data:{
        session_day_subject_actvity:{heart_activity:"--",
                                        immune_activity:"--",
                                        current_heart_pay:"--",
                                        current_immmune_pay:"--",
                                        current_heart_earnings:"--",
                                        current_immune_earnings:"--",
                                        current_total_earnings:"--",
                                        heart_maintenance_minutes:"--",
                                        immune_maintenance_hours:"--", 
                                        heart_improvment_minutes:{target_activity: "--",target_minutes:"--" , target_bpm:"--"},
                                        immune_improvment_hours:{target_activity: "--",target_hours:"--"},   
                                        time_on_wrist:"--",

                                        },
        session_day_subject_actvity_previous:{heart_activity_minutes:"--",
                                                immune_activity_hours:"--",
                                                time_on_wrist:"--",},
        graph_parameters:{},
        {%if session_treatment == "I"%}
        payMeButtonText : 'Pay Me <i class="fab fa-paypal fa-lg"></i>',
        {%else%}
        payMeButtonText : 'Check In <i class="fas fa-check"></i>',
        {%endif%}
        refreshButtonText : '<i class="fas fa-sync fa-spin"></i>',
        toggleState:"heart",
        session_complete:false,
        session_canceled:false,
        fitbitError:false,
        consent_required:false,
        consent_signature:"",
        questionnaire1_required:false,
        questionnaire2_required:false,
        consent_form_text:"",
        session_date:"--/--/----",
        session_last_day:false,
        paymentError:false,
        status:"success",
        questionnaire1_ids : {{session_subject_questionnaire1_form_ids|safe|escape}},
        questionnaire2_ids : {{session_subject_questionnaire2_form_ids|safe|escape}},          
        helpText:"",             
        helpTitle:"Help",    
        heart_help_text:`{{heart_help_text|safe}}`, 
        immune_help_text:`{{immune_help_text|safe}}`, 
        payment_help_text:`{{payment_help_text|safe}}`,   
        fitbit_link:"",
        fitBitLastSynced:"---",
        fitBitTimeRequired:"---",
        fitbitSyncedToday:false,
        fitBitTimeRequirementMet:true,
        notification_title:"",
        notification_text:"",
        session_treatment:"",
        viewed_heart:false,
        viewed_immune:false,
        payment_toggle_background : "lightgrey",
        payment_available : true,
        soft_delete:false,
        show_averages : false,
        average_heart_score: "---",
        average_sleep_score: "---",
        current_daily_pay: "---",
        current_block_length: "---",
        current_missed_days: "---",
        current_earnings: "---",
    },

    methods:{

        getSessionDaySubject:function(){                    
            
            axios.post('/subjectHome/{{id}}/', {
                            action :"getSessionDaySubject" ,                                                                                                                                                                
                        })
                        .then(function (response) {     
                            app.$data.status = response.data.status;

                            app.$data.soft_delete = response.data.soft_delete;

                            if(app.$data.status != "fail")
                            {
                                app.updateSessionDaySubject(response);    
                                app.$data.refreshButtonText = '<i class="fas fa-sync"></i>';  
                                
                                app.$data.session_complete = response.data.session_complete;                                       
                                app.$data.session_last_day = response.data.session_last_day;
                                app.$data.fitBitTimeRequired = response.data.fitBitTimeRequired;
                                app.$data.fitBitTimeRequirementMet = response.data.fitBitTimeRequirementMet;

                                app.$data.show_averages = response.data.show_averages;
                                app.$data.average_heart_score = response.data.average_heart_score;
                                app.$data.average_sleep_score = response.data.average_sleep_score;
                                app.$data.current_daily_pay = response.data.current_daily_pay;
                            }
                            else
                            {
                                app.$data.refreshButtonText = '<i class="fas fa-exclamation-circle"></i>';                                
                            }

                            app.$data.consent_required = response.data.consent_required;
                            app.$data.consent_form_text = response.data.consent_form_text;
                            app.$data.questionnaire1_required = response.data.questionnaire1_required;
                            app.$data.questionnaire2_required = response.data.questionnaire2_required;
                            app.$data.fitbit_link = response.data.fitbit_link;  
                            app.$data.fitbitError = response.data.fitbitError;       
                            app.$data.fitBitLastSynced = response.data.fitBitLastSynced;      
                            app.$data.fitbitSyncedToday = response.data.fitbitSyncedToday;               

                            if(!app.$data.soft_delete)
                            {
                                app.toggleConsentForm();
                                app.toggleQuesionnaire1();
                                app.toggleQuesionnaire2();
                                app.toogleNotification();
                                
                            }                                 

                            if(app.$data.toggleState == 'heart')
                            {
                                app.$data.viewed_heart = true;
                            }
                            else
                            {
                                app.$data.viewed_heart = false;
                            }

                            if(app.$data.toggleState == 'immune')
                            {
                                app.$data.viewed_immune = true;
                            }
                            else
                            {
                                app.$data.viewed_immune = false;
                            }
                                                                    
                        })
                        .catch(function (error) {
                            console.log(error);
                        });                        
        },

        submitQuestionnaire1:function(){                    
            
            axios.post('/subjectHome/{{id}}/', {
                            action :"submitQuestionnaire1" ,      
                            formData : $("#questionnaire1Form").serializeArray(),                                                                                                                                                          
                        })
                        .then(function (response) {     
                            status=response.data.status;                               

                            app.clearMainFormErrors();

                            if(status=="success")
                            {
                                app.$data.questionnaire1_required = response.data.questionnaire1_required;
                                app.toggleQuesionnaire1();
                                app.toggleQuesionnaire2();
                                app.toogleNotification();
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

        submitQuestionnaire2:function(){                    
            
            axios.post('/subjectHome/{{id}}/', {
                            action :"submitQuestionnaire2" ,      
                            formData : $("#questionnaire2Form").serializeArray(),                                                                                                                                                          
                        })
                        .then(function (response) {     
                            status=response.data.status;                               

                            app.clearMainFormErrors();

                            if(status=="success")
                            {
                                app.$data.questionnaire2_required = response.data.questionnaire2_required;
                                app.toggleQuesionnaire2();
                                app.toogleNotification();
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

        getSessionDaySubjectButton:function()
        {
            app.$data.refreshButtonText = '<i class="fas fa-sync fa-spin"></i>';
            app.getSessionDaySubject();
        },
        
        updateSessionDaySubject:function(response){
            app.$data.session_day_subject_actvity = response.data.session_day_subject_actvity;

            app.$data.session_date = response.data.session_date;
            app.$data.notification_title = response.data.notification_title;
            app.$data.notification_text = response.data.notification_text;

            if (response.data.session_day_subject_actvity_previous)
                app.$data.session_day_subject_actvity_previous=response.data.session_day_subject_actvity_previous;

            if (app.$data.session_day_subject_actvity)
            {
                app.$data.graph_parameters = response.data.graph_parameters;      
                
                Vue.nextTick(app.updateCanvases());          
            }
        },   

        toggleConsentForm:function()
        {
            if(app.$data.consent_required)
            {
                $('#consentModal').modal({backdrop: 'static', keyboard: false}).show();
            }
            else
            {
                if(($("#consentModal").data('bs.modal') || {})._isShown)
                {
                    $('#consentModal').modal('toggle');
                }
            } 
        },

        toggleQuesionnaire1:function()
        {                    
            if(app.$data.questionnaire1_required && !app.$data.consent_required)
            {
                $('#questionnaire1Modal').modal({backdrop: 'static', keyboard: false}).show();
            }
            else
            {
                if(($("#questionnaire1Modal").data('bs.modal') || {})._isShown)
                {
                    $('#questionnaire1Modal').modal('toggle');
                }
            } 
        },

        toggleQuesionnaire2:function()
        {                    
            if(app.$data.questionnaire2_required &&
                !app.$data.consent_required &&
                !app.$data.questionnaire1_required &&
                app.session_last_day)
            {
                $('#questionnaire2Modal').modal({backdrop: 'static', keyboard: false}).show();
            }
            else
            {
                if(($("#questionnaire2Modal").data('bs.modal') || {})._isShown)
                {
                    $('#questionnaire2Modal').modal('toggle');
                }
            } 
        },

        toogleNotification:function(){
            if(!app.$data.questionnaire2_required &&
                !app.$data.consent_required &&
                !app.$data.questionnaire1_required &&
                app.$data.notification_text != ""
                )
            {

                app.$data.helpTitle = app.$data.notification_title;
                app.$data.helpText = app.$data.notification_text;
                $('#helpModal').modal('show');
        
            }
        },

        acceptConsentForm:function(){

            if(app.$data.consent_signature=="")
            {
                alert("Please type your full name.")
                return;
            }

            axios.post('/subjectHome/{{id}}/', {
                            action :"acceptConsentForm",   
                            consent_signature : app.$data.consent_signature,                                                                                                                                                             
                        })
                        .then(function (response) {    
                            
                            app.$data.consent_required = response.data.consent_required;
                            app.toggleConsentForm();
                            app.toggleQuesionnaire1();
                            app.toggleQuesionnaire2();
                            app.toogleNotification();

                        })
                        .catch(function (error) {
                            console.log(error);                                    
                        });                        
        },

        updateCanvases:function(){
                    
            gp=app.$data.graph_parameters;

            if(app.$data.toggleState == "heart")
            {
            app.drawAxis("healthChart",gp.y_min_heart,gp.y_max_heart,gp.y_ticks_heart,
                                            gp.x_min_heart,gp.x_max_heart,gp.x_ticks_heart,
                                            "Tomorrow's Heart Health Score","Today's Zone Minutes");
            
            app.drawLine("healthChart",gp.y_min_heart,gp.y_max_heart,
                                            gp.x_min_heart,gp.x_max_heart,
                                            app.$data.session_day_subject_actvity.heart_activity_future,0,"crimson");
            }
            else
            {
            app.drawAxis("healthChart",gp.y_min_immune,gp.y_max_immune,gp.y_ticks_immune,
                                            gp.x_min_immune,gp.x_max_immune,gp.x_ticks_immune,
                                            "Tomorrow's Sleep Health Score","Today's Hours Sleeping");    

            app.drawLine("healthChart",gp.y_min_immune,gp.y_max_immune,
                                            gp.x_min_immune*60,gp.x_max_immune*60,
                                            app.$data.session_day_subject_actvity.immune_activity_future,0,"cornflowerBlue");  
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

            var canvas = document.getElementById(chartID),
                ctx = canvas.getContext('2d');           

            var w =  ctx.canvas.width;
            var h = ctx.canvas.height;
            var marginY=45;
            var marginX=40;
            var margin2=10;
            var tickLength=3;

            ctx.save();

            ctx.translate(marginY, h-marginX);
            ctx.moveTo(0, 0);

            ctx.beginPath();
            for(i=0;i<dataSet.length;i++)
            {
                x = app.convertToX(dataSet[i].x,xMax,xMin,w-marginY-margin2,markerWidth);
                y = app.convertToY(dataSet[i].y,yMax,yMin,h-marginX-margin2,markerWidth);

                ctx.lineTo(x,y);
            }    

            ctx.strokeStyle=markerColor;
            ctx.lineWidth=markerWidth;
            ctx.stroke();    
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

        updateToogleState:function(toggleState){
            app.$data.toggleState = toggleState;

            if(app.$data.toggleState == 'heart')
            {
                app.$data.viewed_heart = true;
            }                    

            if(app.$data.toggleState == 'immune')
            {
                app.$data.viewed_immune = true;
            }                    

            Vue.nextTick(app.updateCanvases());    
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
            for(i=0;i<app.$data.questionnaire1_ids.length;i++)
            {
                item = app.$data.questionnaire1_ids[i];
                $("#id_" + item).attr("class","form-control");
                $("#id_errors_" + item).remove();
            }

            for(i=0;i<app.$data.questionnaire2_ids.length;i++)
            {
                item = app.$data.questionnaire2_ids[i];
                $("#id_" + item).attr("class","form-control");
                $("#id_errors_" + item).remove();
            }

            for(var item in app.$data.questionnaire2_ids)
            {
                $("#id_" + item).attr("class","form-control");
                $("#id_errors_" + item).remove();
            }

        },

        showHelpBox:function(){                

            if(app.$data.toggleState=='heart')
            {
                app.$data.helpTitle = "Heart Help"
                app.$data.helpText = app.$data.heart_help_text;
            }
            else if(app.$data.toggleState=='immune')
            {
                app.$data.helpTitle = "Sleep Help"
                app.$data.helpText = app.$data.immune_help_text;
            }
            else if (app.$data.toggleState == 'payment')
            {
                app.$data.helpTitle = "Payment Help"
                app.$data.helpText = app.$data.payment_help_text;
            }

            $('#helpModal').modal('show');                   
        },

        hideHelpBox:function(){
            app.$data.helpText="";
        },   
        
        {%if session_treatment == "I"%}
            {%include "subject/home/individual_payment.js"%}
        {%else%}
            {%include "subject/home/A_B_C_check_in.js"%}
        {%endif%}
    },

    mounted: function(){
        {%if status == "success" %}
            this.getSessionDaySubject();      
            $('#hideHelpBox').on("hidden.bs.modal", this.hideHelpBox);   
        {%endif%}             
    },
});