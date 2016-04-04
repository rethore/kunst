import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';
import { Hue } from '../imports/api/hue.js';

import './main.html';


const IP = 'ip322.alb283.cust.comxnet.dk:6785';

Template.hello.onCreated(function helloOnCreated() {
  // counter starts at 0
  this.counter = new ReactiveVar(0);
});

Template.hello.helpers({
  counter() {
    return Template.instance().counter.get();
  },
});

Template.hello.events({
  'click button'(event, instance) {
    // increment the counter when button is clicked
    instance.counter.set(instance.counter.get() + 1);
  },
});

Template.production.rendered=function() {
	$('#my-datepicker').datepicker();
}

Template.sunshow.helpers({
  disabled() {return (Hue.findOne({name:'active'}))? (Hue.findOne({name:'active'}).val)? "disabled" : "" : ""},
  colormaps: [{cname:"gist_gray"},
          {cname:"RdPu_r"},
          {cname:"Set3_r"},
          {cname:"gray"},
          {cname:"Set2"},
          {cname:"gist_ncar_r"},
          {cname:"gist_ncar"},
          {cname:"Accent"},
          {cname:"YlGn"},
          {cname:"RdYlBu"},
          {cname:"BrBG_r"},
          {cname:"Pastel2_r"},
          {cname:"YlGn_r"},
          {cname:"hot_r"},
          {cname:"YlOrRd_r"},
          {cname:"Spectral_r"},
          {cname:"BrBG"},
          {cname:"Purples"},
          {cname:"terrain_r"},
          {cname:"PuRd"},
          {cname:"summer_r"},
          {cname:"gist_heat"},
          {cname:"flag_r"},
          {cname:"gist_earth_r"},
          {cname:"PuBuGn"},
          {cname:"PuBu"},
          {cname:"gist_gray_r"},
          {cname:"hsv_r"},
          {cname:"binary_r"},
          {cname:"PiYG_r"},
          {cname:"gist_yarg"},
          {cname:"OrRd"},
          {cname:"GnBu_r"},
          {cname:"coolwarm_r"},
          {cname:"RdYlGn"},
          {cname:"spectral"},
          {cname:"Wistia_r"},
          {cname:"Dark2"},
          {cname:"PuOr_r"},
          {cname:"PiYG"},
          {cname:"seismic"},
          {cname:"RdPu"},
          {cname:"Spectral"},
          {cname:"Reds"},
          {cname:"Oranges_r"},
          {cname:"nipy_spectral"},
          {cname:"Blues"},
          {cname:"YlOrBr_r"},
          {cname:"gist_stern_r"},
          {cname:"CMRmap"},
          {cname:"PRGn_r"},
          {cname:"Greens_r"},
          {cname:"BuGn_r"},
          {cname:"RdBu"},
          {cname:"nipy_spectral_r"},
          {cname:"PuRd_r"},
          {cname:"Accent_r"},
          {cname:"jet_r"},
          {cname:"BuPu"},
          {cname:"Set1"},
          {cname:"gist_rainbow"},
          {cname:"gnuplot2_r"},
          {cname:"Reds_r"},
          {cname:"Greys_r"},
          {cname:"prism"},
          {cname:"rainbow"},
          {cname:"Purples_r"},
          {cname:"bwr_r"},
          {cname:"Pastel1"},
          {cname:"YlGnBu_r"},
          {cname:"gist_yarg_r"},
          {cname:"spectral_r"},
          {cname:"hot"},
          {cname:"RdGy_r"},
          {cname:"gist_earth"},
          {cname:"spring"},
          {cname:"RdBu_r"},
          {cname:"bone"},
          {cname:"BuPu_r"},
          {cname:"cubehelix"},
          {cname:"autumn"},
          {cname:"PuOr"},
          {cname:"brg"},
          {cname:"brg_r"},
          {cname:"RdGy"},
          {cname:"bwr"},
          {cname:"Dark2_r"},
          {cname:"Pastel2"},
          {cname:"cool_r"},
          {cname:"copper"},
          {cname:"PuBuGn_r"},
          {cname:"afmhot_r"},
          {cname:"binary"},
          {cname:"OrRd_r"},
          {cname:"YlOrRd"},
          {cname:"hsv"},
          {cname:"afmhot"},
          {cname:"gist_stern"},
          {cname:"gnuplot"},
          {cname:"Blues_r"},
          {cname:"rainbow_r"},
          {cname:"Pastel1_r"},
          {cname:"gnuplot_r"},
          {cname:"YlGnBu"},
          {cname:"PRGn"},
          {cname:"gray_r"},
          {cname:"bone_r"},
          {cname:"prism_r"},
          {cname:"BuGn"},
          {cname:"PuBu_r"},
          {cname:"RdYlGn_r"},
          {cname:"CMRmap_r"},
          {cname:"YlOrBr"},
          {cname:"pink_r"},
          {cname:"Paired_r"},
          {cname:"Greens"},
          {cname:"pink"},
          {cname:"spring_r"},
          {cname:"seismic_r"},
          {cname:"Set1_r"},
          {cname:"Oranges"},
          {cname:"RdYlBu_r"},
          {cname:"cubehelix_r"},
          {cname:"jet"},
          {cname:"ocean_r"},
          {cname:"terrain"},
          {cname:"copper_r"},
          {cname:"flag"},
          {cname:"ocean"},
          {cname:"GnBu"},
          {cname:"winter"},
          {cname:"winter_r"},
          {cname:"autumn_r"},
          {cname:"gist_heat_r"},
          {cname:"cool"},
          {cname:"gnuplot2"},
          {cname:"Wistia"},
          {cname:"Set2_r"},
          {cname:"Set3"},
          {cname:"Paired"},
          {cname:"coolwarm"},
          {cname:"summer"},
          {cname:"gist_rainbow_r"},
          {cname:"Greys"}]});

Template.sunshow.events({
  'click .cmap'(event, instance){
    event.preventDefault();
    let cmap=event.target.id;
    console.log(cmap, event, instance);
    Meteor.call("hue.activate");
    //event.preventDefaults();
    HTTP.get(`http://${IP}/sun/${cmap}`, function(error, result){
      if(error){
        console.log("error", error);
      }
      if(result){
         console.log("result", result)
         if (result.content === "done") {
           Meteor.call("hue.deactivate");
         }
      }
    });
  },
  'click .defaultshow'(event, instance){
    event.preventDefault();
    let cmap='hot';
    console.log(cmap, event, instance);
    Meteor.call("hue.activate");
    //event.preventDefaults();
    HTTP.get(`http://${IP}/sun/${cmap}`, function(error, result){
      if(error){
        console.log("error", error);
      }
      if(result){
         console.log("result", result)
         if (result.content === "done") {
           Meteor.call("hue.deactivate");
         }
      }
    });
  },
})




Template.rungame.helpers({
    disabled() {return (Hue.findOne({name:'active'}))?
        (Hue.findOne({name:'active'}).val)? "disabled" : "" : ""}
});

Template.rungame.events({
  'click button'(event, instance){
    Meteor.call("hue.activate");
    let speed = $('#speed').val();
    let tours = $('#tours').val();
    let url = `http://${IP}/run/${speed}/${tours}`;
    console.log(event, instance, url, speed);
    //event.preventDefaults();
    HTTP.get(url, function(error, result){
      if(error){
        console.log("error", error);
      }
      if(result){
         console.log("result", result)
         if (result.content === "done") {
           Meteor.call("hue.deactivate");
         }
      }
    });
  },
})

Template.lamps.events({
  'click .glyphicon-refresh'(event, instance){
      console.log('click!');
  }
});
