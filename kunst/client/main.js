import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';
import { Hue } from '../imports/api/hue.js';

import './main.html';


var colormaps = [{cname:"gist_gray"},
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
        {cname:"Greys"}];

Session.setDefault("date", [4,4,2016]);



Meteor.startup(() => {
  $('#my-datepicker').val(Session.get('date'))
})

Template.body.onCreated(function bodyOnCreated() {
  Meteor.subscribe('hue');
});

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
	$('#my-datepicker').datepicker({format: "d/m/yyyy"});
  let [day, month, year] = Session.get('date')
  $('#my-datepicker').val(`${day}/${month}/${year}`)
}

Template.production.helpers({
  disabled() {return (Hue.findOne({name:'active'}))? (Hue.findOne({name:'active'}).val)? "disabled" : "" : ""},
  date() {
    let [day, month, year] = Session.get('date')
    return `${day}/${month}/${year}`
  },
  url(){
    let date = $('#my-datepicker').val();
    let [day, month, year] = Session.get('date');
    let data = Hue.findOne({name:'data', day, month, year});
    console.log('data',date)
    return (data)? data.url : 'https://plot.ly/~piredtu/36';
    //return 'https://plot.ly/~piredtu/36';
  }
});

Template.production.events({
  'click #getdate'(event, instance){
    console.log(Session.get('date'));
    let date = $('#my-datepicker').val();
    let [day, month, year] = date.split('/')
    Session.set('date', [day, month, year])
    console.log(date, day, month, year)
    if (!Hue.findOne({name:'data', day, month, year})) {
      Meteor.call("download", day, month, year)
    }
  }
});

Template.sunshow.helpers({
  disabled() {return (Hue.findOne({name:'active'}))? (Hue.findOne({name:'active'}).val)? "disabled" : "" : ""},
  panelstatus() {return (Hue.findOne({name:'active'}))? (Hue.findOne({name:'active'}).panel == 'sunshow')? "panel-success" : "panel-default" : "panel-default"},
  date() {
    let a = Hue.findOne({name:'active'});
    let [day, month, year] = Session.get('date');
    return (a)? (a.val)? a.data : {day, month, year} : {day, month, year};
  },
  colormaps: colormaps,
});

Template.sunshow.events({
  'click .cmap'(event, instance){
    event.preventDefault();
    let cmap=event.target.id;
    let [day, month, year] = Session.get('date')
    Meteor.call("sunshow", cmap, day, month, year);
  },
  'click .defaultshow'(event, instance){
    event.preventDefault();
    let cmap='hot';
    let [day, month, year] = Session.get('date')
    Meteor.call("sunshow", cmap, day, month, year);
  },
})

Template.rungame.helpers({
    disabled() {return (Hue.findOne({name:'active'}))?
        (Hue.findOne({name:'active'}).val)? "disabled" : "" : ""},
    panelstatus() {return (Hue.findOne({name:'active'}))?
        (Hue.findOne({name:'active'}).panel == 'rungame')? "panel-success" : "panel-default" : "panel-default"},
});

Template.rungame.events({
  'click button'(event, instance){
    let speed = $('#speed').val();
    let tours = $('#tours').val();
    //event.preventDefaults();
    Meteor.call("rungame", speed, tours)
  },
})

Template.lamps.events({
  'click .glyphicon-refresh'(event, instance){
      console.log('click!');
  },
  'click #reactivate'(event, instance){Meteor.call("hue.deactivate")},
  'click #on'(event, instance){Meteor.call('on')},
  'click #off'(event, instance){Meteor.call('off')},
  'click #none'(event, instance){
      event.preventDefault();
      console.log('click!');
      Meteor.call('effect','none');},
  'click #colorloop'(event, instance){
      event.preventDefault();
      Meteor.call('effect','colorloop');
    },
});

Template.lamps.helpers({
  huecontrol: () => Hue.findOne({name:'heartbeat'}).val,
  panelstatus: () => (Hue.findOne({name:'heartbeat'}))? (Hue.findOne({name:'heartbeat'}).val)? "panel-success" : "panel-danger" : "panel-warning",
});
