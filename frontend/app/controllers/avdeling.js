import Ember from 'ember';

export default Ember.Controller.extend({
  queryParams: [
    'q',
  ],

  actions: {
    search() {
      let query = event.target.value;
      this.set('q', query);
    },

    searchButton(searchString) {
      this.set('q', searchString);
    },
  }
});
