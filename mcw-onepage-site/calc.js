/* MCW revenue calculator maths (pure, testable with node). */
(function (root) {
  'use strict';
  function compute(i) {
    var keys = ['machines', 'rent', 'turns', 'price', 'utilities', 'investment'];
    for (var k = 0; k < keys.length; k++) {
      var v = i[keys[k]];
      if (v === '' || v === null || v === undefined || !isFinite(Number(v)) || Number(v) < 0) return { ok: false };
    }
    var m = Number(i.machines), rent = Number(i.rent), turns = Number(i.turns), price = Number(i.price),
        util = Number(i.utilities), inv = Number(i.investment);
    if (m < 1 || m > 12) return { ok: false };
    var dayRev = m * turns * price, monthRev = dayRev * 30, yearRev = monthRev * 12;
    var monthNet = monthRev - rent - util, dayNet = monthNet / 30, yearNet = monthNet * 12;
    var payback = monthNet > 0 ? inv / monthNet : null;
    return { ok: true, dayRev: dayRev, monthRev: monthRev, yearRev: yearRev, dayNet: dayNet, monthNet: monthNet, yearNet: yearNet, payback: payback };
  }
  var api = { compute: compute };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.MCWCalc = api;
})(this);
