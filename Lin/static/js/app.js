//  Target url

let jsonUrl = "https://2u-data-curriculum-team.s3.amazonaws.com/dataviz-classroom/v1.1/14-Interactive-Web-Visualizations/02-Homework/samples.json"

let outputUrl = '../../OutputData'
// Read data from json url

d3.json(jsonUrl).then(function (data) {

    //Create and append select list

    let selectList = document.getElementById("selDataset");

    //Create and append the options

    for (let i = 0; i < data['names'].length; i++) {
        var option = document.createElement("option");
        option.value = data['names'][i];
        option.text = data['names'][i];
        selectList.appendChild(option);
    }
});


// Create function to trigger change

function optionChanged(id){

    d3.json(jsonUrl).then(function (data) {
    
        // Taget index of id to source the data

        index = data['names'].indexOf(id);
        
        // Use Plotly to plot a bar plot

        traceBar = {
                x:data['samples'][index]['sample_values'].slice(0,10).reverse(),
                y:data['samples'][index]['otu_ids'].slice(0,10).map(num => {return String('OTU'+num)}).reverse(),
                text:data['samples'][index]['otu_labels'].slice(0,10).reverse(),
                type: "bar",
                orientation: "h"
        };


        // //////////////////////////////////////////////////////////////////////////////////////////////

        // Display Ids'details

        traceDataBar = [traceBar];
     
        let layoutBar = {
                height: 600,
                width: 500,
                margin:{
                    l: 100,
                    r: 100,
                    b: 100,
                    t: 1
                }
        };
       
        Plotly.newPlot("bar",traceDataBar,layoutBar);


        // Reset innerHTML 

        document.getElementById("sample-metadata").innerHTML ='';


        // Display Ids'details

        let keys= Object.keys(data['metadata'][index]);

        let values= Object.values(data['metadata'][index]);

        for (let i = 0; i < keys.length; i++) {
            
            let idDetail= `<h5>${keys[i].charAt(0).toUpperCase()+ keys[i].slice(1)}: ${values[i]}</h5>`;
            
            document.getElementById("sample-metadata").innerHTML += idDetail;}


       
        // //////////////////////////////////////////////////////////////////////////////////////////////

        // Use Plotly to plot a bubble plot

        traceBubble= {
        
            mode: 'markers',
            x:data['samples'][index]['otu_ids'],
            y:data['samples'][index]['sample_values'],
            marker:{
                size:data['samples'][index]['sample_values'],
                color:data['samples'][index]['otu_ids'],
                },
            text:data['samples'][index]['otu_labels'].slice(0,10).reverse(),
            type: "bubble"
           
        };
    
        traceDataBubble = [traceBubble];

        let layoutBubble = {

            margin:{
                l: 100,
                r: 100,
                b: 100,
                t: 1
            },

            xaxis: {
                title: {
                  text: 'OTU ID',
                  font: {size: 18}
                },
            },
      };
        
        Plotly.newPlot("bubble",traceDataBubble,layoutBubble);  


        // //////////////////////////////////////////////////////////////////////////////////////////////

        // Use Plotly to plot a Donut plot

        var traceDonut = {

            type: "pie",
            showlegend: false,
            hole: 0.4,
            rotation: 90,
            values: [9, 9, 9, 9, 9, 9, 9, 9, 9, 81 ],
            text: ['0-1','1-2','2-3','3-4','4-5','5-6','6-7','7-8','8-9',''],
            direction: "clockwise",
            textinfo: "text",
            textposition: "inside",
            marker: {
                colors: ["#ddead1", "#c7ddb5","#b3cf99","a3c585","95bb72",
                        "87ab69","#75975e", "#658354", "#4b6043",'white']
            },
            labels: ['0-1','1-2','2-3','3-4','4-5','5-6','6-7','7-8','8-9',''],
            
        };

        // Insert needle and use wfreq as indicator

        let indicator = data['metadata'][index]['wfreq'];

        var radius = 0.2;

        var radians = 0.175+0.349*indicator;

        let x=Math.cos(radians)*radius;

        let y=Math.sin(radians)*radius;
        
        var layoutDonut = {

            shapes:[{
                    type: 'line',
                    x0: 0.5,
                    y0: 0.5,
                    x1: 0.5-x,
                    y1: 0.5+y,
                    line: {color: 'black',width: 3}
            }],
            

            title: '<b>Belly Button Washing Frequncy</b> <br> Scrub per Week',

            font: {
                size: 18,
                fontWeight:"bold"
            },

            height:450,
            
            width: 500,

            hovermode: false,
        }; 

        var traceDataDonut = [traceDonut];

        Plotly.newPlot('gauge', traceDataDonut, layoutDonut);

    });
};

