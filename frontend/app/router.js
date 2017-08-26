import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route('search', {path: '/'});
  this.route('avdeling');
  this.route('lookupAnsatt', {path: '/ansatt/:person_id'});
  this.route('lookupAvdeling', {path: '/avdeling/:department_id'});
});

export default Router;
