import Ember from 'ember';

export default Ember.Route.extend({
    actions: {
        loading(transition, route) {
            let controller = this.controllerFor(route.routeName);
            controller.set('isLoading', true);

            transition.finally(() => {
                controller.set('isLoading', false);
            })
        }
    }
});
