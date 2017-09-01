import BaseRoute from '../base';

export default Ember.Route.extend({
  model(params) {
    return this.store.findRecord('person', params.person_id);
  }
});
