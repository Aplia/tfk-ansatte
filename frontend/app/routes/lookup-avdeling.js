import Ember from 'ember';

export default Ember.Route.extend({
  queryParams: {
      q: { refreshModel: true },
  },

  model(params) {
      return this.store.findRecord(
          'department',
          params.department_id,
          {adapterOptions: {query: {q: params.q}}},
      );
  }
});
