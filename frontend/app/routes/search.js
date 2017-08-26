import Ember from 'ember';
import BaseRoute from './base';

export default BaseRoute.extend({
    queryParams: {
        q: { refreshModel: true },
        departmentId: { refreshModel: true },
    },

    model(params) {
        let people = [];
        if (params.q || params.departmentId) {
            people = this.store.query('person', {
                q: params.q,
                department_id: params.departmentId,
            })
        }

        return Ember.RSVP.hash({
            people: people,
            departments: this.get('store').findAll('department'),
        })
    }
});
