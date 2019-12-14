
/**
 * Component to render list of available currencies with radio select
 */
Vue.component('currency-input', {
  props: ['currencies', 'disabledValue', 'value', 'suffix'],
  template: `
  <div>
    <div class="form-check" v-for="cur in currencies">
      <input 
        class="form-check-input" 
        type="radio" 
        v-bind:name="'currency' + suffix" 
        v-bind:checked="cur.code == value"
        v-bind:disabled="cur.code == disabledValue"
        v-bind:value="cur.code"
        v-bind:id="\`currency\${suffix}\${cur.code}\`"
        v-on:change="$emit('input', cur.code)">
      <label 
        class="form-check-label"
        v-bind:for="\`currency\${suffix}\${cur.code}\`">
        {{cur.symbol}} ({{cur.code}})
      </label>
    </div>
  </div>
  `
});

var app = new Vue({
  el: '#appContainer',
  data: {
    currencies: [
      {
        symbol: '€',
        code: 'EUR'
      },
      {
        symbol: '$',
        code: 'USD'
      },
      {
        symbol: '¥',
        code: 'JPY'
      }
    ],
    currencyTo: 'EUR',
    currencyFrom: 'USD',
    amountFrom: 10,
    amountTo: '...'
  },
  computed: {
    /**
     * Conversion direction
     * 
     * I use computed property for watcher 
     * Otherwise it can trigger twice when you swap conversion direction.
     */
    conversion: function () {
      return [this.currencyTo, this.currencyFrom]
    }
  },
  methods: {
    /**
     * Find symbol by currency code
     * 
     * @param {string} curencyCode 3-letter code
     * @returns {string} symbol
     */
    getCurrencySymbol: function(curencyCode) {
      var currency = _.find(this.currencies, val => val.code === curencyCode)
      return currency.symbol;
    },

    /**
     * Change currency conversion direction (swaps To and From)
     */
    swapCurrency() {
      [this.currencyFrom, this.currencyTo] = [this.currencyTo, this.currencyFrom]
    },

    /**
     * Do an API call to calculate amount in foreign currency
     */
    getConvertedCurrency() {
      this.amountTo = '...';
      
      fetch('/api/convert/', {
        method:'POST', 
        body: JSON.stringify({
          from: this.currencyFrom, 
          to: this.currencyTo, 
          amount: parseFloat(this.amountFrom)
        })
      }).then(
        r => r.json()
      ).then(
        data => {
          this.amountTo = data.result.toFixed(2);
        }
      )

    }
  },
  /**
   * Handle conversion of initial data
   */
  created: function () {
    this.debouncedGetRate = _.debounce(this.getConvertedCurrency, 500);
    this.getConvertedCurrency();
  },
  watch: {
    /**
     * When conversion direction is changed I run API code immediately
     */
    conversion: function () {
      this.getConvertedCurrency();
    },
    /**
     * When user types new amount I wait 500 msec to finish typing
     * 
     * So when user types `150` it does not fire 3 requests for `1`, `15` and `150`
     */
    amountFrom: function () {
      this.amountTo = '...';
      this.debouncedGetRate();
    }
  }
})