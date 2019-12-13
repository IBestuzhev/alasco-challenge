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
      conversion: function () {
        // Use computed property for watcher 
        // Otherwise it can trigger twice when you swap conversion direction.
        return [this.currencyTo, this.currencyFrom]
      }
    },
    methods: {
      getCurrencySymbol: function(curencyCode) {
        var currency = _.find(this.currencies, val => val.code === curencyCode)
        return currency.symbol;
      },
      swapCurrency() {
        [this.currencyFrom, this.currencyTo] = [this.currencyTo, this.currencyFrom]
      },
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
    created: function () {
      this.debouncedGetRate = _.debounce(this.getConvertedCurrency, 500);
      this.getConvertedCurrency();
    },
    watch: {
      conversion: function () {
        this.getConvertedCurrency();
      },
      amountFrom: function () {
        this.amountTo = '...';
        this.debouncedGetRate();
      }
    }
  })