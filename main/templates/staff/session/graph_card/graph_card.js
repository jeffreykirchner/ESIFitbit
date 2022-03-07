//update graph after toggle state change
updateToogleState:function(toggleState){
    app.$data.toggleState = toggleState;
    Vue.nextTick(app.updateCanvases());    
},

//update canvas with current toggle state
updateCanvases(){

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

//draw graph axis
drawAxis(chartID,yMin,yMax,yTickCount,xMin,xMax,xTickCount,yLabel,xLabel){

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

//draw line givin data set
drawLine(chartID,yMin,yMax,xMin,xMax,dataSet,markerWidth,markerColor){

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

//convert value into x cordinate
convertToX(tempValue,maxValue,minValue,tempWidth, markerWidth){
    tempT = tempWidth / (maxValue-minValue);

    tempValue-=minValue;

    if(tempValue>maxValue) tempValue=maxValue;

    return (tempT * tempValue - markerWidth/2);
},

//convert value into y cordinate
convertToY(tempValue,maxValue,minValue,tempHeight, markerHeight){
    tempT = tempHeight / (maxValue-minValue);

    if(tempValue > maxValue) tempValue=maxValue;
    if(tempValue < minValue) tempValue=minValue;

    tempValue-=minValue;

    if(tempValue>maxValue) tempValue=maxValue;

    return(-1 * tempT * tempValue - markerHeight/2)
},