import BaseRoute from '../base';

export default BaseRoute.extend({
    queryParams: {
        q: { refreshModel: true },
    },

    model(params) {
        if (params.q) {
            return this.store.query('department', {
                q: params.q
            })
        } else {
            return this.store.findAll('department');
        }
    },
});
