import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route('employees', {path: '/'}, function() {
    this.route('employee', {path: '/ansatt/:person_id'});
  });
  this.route('departments', {path: '/avdelinger'}, function() {
    this.route('department', {path: '/avdelinger/:department_id'});
  });
});

export default Router;
