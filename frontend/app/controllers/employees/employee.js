import Ember from 'ember';

export default Ember.Controller.extend({
    actions: {
        goBack() {
            history.back();
        }
    }
});
