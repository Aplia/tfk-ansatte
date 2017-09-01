import BaseRoute from '../base';

export default BaseRoute.extend({
    queryParams: {
        q: {refreshModel: true},
    },

    model(params) {
        return this.store.findRecord(
            'department',
            params.department_id,
            {
                reload: true,
                adapterOptions: {query: {q: params.q}},
            },
        );
    }
});
