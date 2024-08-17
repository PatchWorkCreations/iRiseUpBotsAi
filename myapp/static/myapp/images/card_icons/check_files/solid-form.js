!function (e) {
  "function" == typeof define && define.amd ? define(e) : e();
}(function () {
  "use strict";

  function e(e, t, n) {
    if ("function" == typeof e ? e === t : e.has(t)) return arguments.length < 3 ? t : n;
    throw new TypeError("Private element is not present on this object");
  }
  function t(e, t, n) {
    return t = v(t), function (e, t) {
      if (t && ("object" == typeof t || "function" == typeof t)) return t;
      if (void 0 !== t) throw new TypeError("Derived constructors may only return object or undefined");
      return function (e) {
        if (void 0 === e) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
        return e;
      }(e);
    }(e, i() ? Reflect.construct(t, n || [], v(e).constructor) : t.apply(e, n));
  }
  function n(t, n) {
    return t.get(e(t, n));
  }
  function r(t, n, r) {
    return t.set(e(t, n), r), r;
  }
  function i() {
    try {
      var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function () {}));
    } catch (t) {}
    return (i = function () {
      return !!e;
    })();
  }
  function o(e, t) {
    var n = Object.keys(e);
    if (Object.getOwnPropertySymbols) {
      var r = Object.getOwnPropertySymbols(e);
      t && (r = r.filter(function (t) {
        return Object.getOwnPropertyDescriptor(e, t).enumerable;
      })), n.push.apply(n, r);
    }
    return n;
  }
  function a(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = null != arguments[t] ? arguments[t] : {};
      t % 2 ? o(Object(n), !0).forEach(function (t) {
        p(e, t, n[t]);
      }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : o(Object(n)).forEach(function (t) {
        Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(n, t));
      });
    }
    return e;
  }
  function s() {
    s = function () {
      return t;
    };
    var e,
      t = {},
      n = Object.prototype,
      r = n.hasOwnProperty,
      i = Object.defineProperty || function (e, t, n) {
        e[t] = n.value;
      },
      o = "function" == typeof Symbol ? Symbol : {},
      a = o.iterator || "@@iterator",
      u = o.asyncIterator || "@@asyncIterator",
      c = o.toStringTag || "@@toStringTag";
    function l(e, t, n) {
      return Object.defineProperty(e, t, {
        value: n,
        enumerable: !0,
        configurable: !0,
        writable: !0
      }), e[t];
    }
    try {
      l({}, "");
    } catch (R) {
      l = function (e, t, n) {
        return e[t] = n;
      };
    }
    function f(e, t, n, r) {
      var o = t && t.prototype instanceof m ? t : m,
        a = Object.create(o.prototype),
        s = new L(r || []);
      return i(a, "_invoke", {
        value: T(e, n, s)
      }), a;
    }
    function h(e, t, n) {
      try {
        return {
          type: "normal",
          arg: e.call(t, n)
        };
      } catch (r) {
        return {
          type: "throw",
          arg: r
        };
      }
    }
    t.wrap = f;
    var d = "suspendedStart",
      p = "suspendedYield",
      g = "executing",
      v = "completed",
      y = {};
    function m() {}
    function b() {}
    function w() {}
    var k = {};
    l(k, a, function () {
      return this;
    });
    var P = Object.getPrototypeOf,
      x = P && P(P(j([])));
    x && x !== n && r.call(x, a) && (k = x);
    var S = w.prototype = m.prototype = Object.create(k);
    function C(e) {
      ["next", "throw", "return"].forEach(function (t) {
        l(e, t, function (e) {
          return this._invoke(t, e);
        });
      });
    }
    function E(e, t) {
      function n(i, o, a, s) {
        var u = h(e[i], e, o);
        if ("throw" !== u.type) {
          var c = u.arg,
            l = c.value;
          return l && "object" == typeof l && r.call(l, "__await") ? t.resolve(l.__await).then(function (e) {
            n("next", e, a, s);
          }, function (e) {
            n("throw", e, a, s);
          }) : t.resolve(l).then(function (e) {
            c.value = e, a(c);
          }, function (e) {
            return n("throw", e, a, s);
          });
        }
        s(u.arg);
      }
      var o;
      i(this, "_invoke", {
        value: function (e, r) {
          function i() {
            return new t(function (t, i) {
              n(e, r, t, i);
            });
          }
          return o = o ? o.then(i, i) : i();
        }
      });
    }
    function T(t, n, r) {
      var i = d;
      return function (o, a) {
        if (i === g) throw Error("Generator is already running");
        if (i === v) {
          if ("throw" === o) throw a;
          return {
            value: e,
            done: !0
          };
        }
        for (r.method = o, r.arg = a;;) {
          var s = r.delegate;
          if (s) {
            var u = O(s, r);
            if (u) {
              if (u === y) continue;
              return u;
            }
          }
          if ("next" === r.method) r.sent = r._sent = r.arg;else if ("throw" === r.method) {
            if (i === d) throw i = v, r.arg;
            r.dispatchException(r.arg);
          } else "return" === r.method && r.abrupt("return", r.arg);
          i = g;
          var c = h(t, n, r);
          if ("normal" === c.type) {
            if (i = r.done ? v : p, c.arg === y) continue;
            return {
              value: c.arg,
              done: r.done
            };
          }
          "throw" === c.type && (i = v, r.method = "throw", r.arg = c.arg);
        }
      };
    }
    function O(t, n) {
      var r = n.method,
        i = t.iterator[r];
      if (i === e) return n.delegate = null, "throw" === r && t.iterator.return && (n.method = "return", n.arg = e, O(t, n), "throw" === n.method) || "return" !== r && (n.method = "throw", n.arg = new TypeError("The iterator does not provide a '" + r + "' method")), y;
      var o = h(i, t.iterator, n.arg);
      if ("throw" === o.type) return n.method = "throw", n.arg = o.arg, n.delegate = null, y;
      var a = o.arg;
      return a ? a.done ? (n[t.resultName] = a.value, n.next = t.nextLoc, "return" !== n.method && (n.method = "next", n.arg = e), n.delegate = null, y) : a : (n.method = "throw", n.arg = new TypeError("iterator result is not an object"), n.delegate = null, y);
    }
    function I(e) {
      var t = {
        tryLoc: e[0]
      };
      1 in e && (t.catchLoc = e[1]), 2 in e && (t.finallyLoc = e[2], t.afterLoc = e[3]), this.tryEntries.push(t);
    }
    function A(e) {
      var t = e.completion || {};
      t.type = "normal", delete t.arg, e.completion = t;
    }
    function L(e) {
      this.tryEntries = [{
        tryLoc: "root"
      }], e.forEach(I, this), this.reset(!0);
    }
    function j(t) {
      if (t || "" === t) {
        var n = t[a];
        if (n) return n.call(t);
        if ("function" == typeof t.next) return t;
        if (!isNaN(t.length)) {
          var i = -1,
            o = function n() {
              for (; ++i < t.length;) if (r.call(t, i)) return n.value = t[i], n.done = !1, n;
              return n.value = e, n.done = !0, n;
            };
          return o.next = o;
        }
      }
      throw new TypeError(typeof t + " is not iterable");
    }
    return b.prototype = w, i(S, "constructor", {
      value: w,
      configurable: !0
    }), i(w, "constructor", {
      value: b,
      configurable: !0
    }), b.displayName = l(w, c, "GeneratorFunction"), t.isGeneratorFunction = function (e) {
      var t = "function" == typeof e && e.constructor;
      return !!t && (t === b || "GeneratorFunction" === (t.displayName || t.name));
    }, t.mark = function (e) {
      return Object.setPrototypeOf ? Object.setPrototypeOf(e, w) : (e.__proto__ = w, l(e, c, "GeneratorFunction")), e.prototype = Object.create(S), e;
    }, t.awrap = function (e) {
      return {
        __await: e
      };
    }, C(E.prototype), l(E.prototype, u, function () {
      return this;
    }), t.AsyncIterator = E, t.async = function (e, n, r, i, o) {
      void 0 === o && (o = Promise);
      var a = new E(f(e, n, r, i), o);
      return t.isGeneratorFunction(n) ? a : a.next().then(function (e) {
        return e.done ? e.value : a.next();
      });
    }, C(S), l(S, c, "Generator"), l(S, a, function () {
      return this;
    }), l(S, "toString", function () {
      return "[object Generator]";
    }), t.keys = function (e) {
      var t = Object(e),
        n = [];
      for (var r in t) n.push(r);
      return n.reverse(), function e() {
        for (; n.length;) {
          var r = n.pop();
          if (r in t) return e.value = r, e.done = !1, e;
        }
        return e.done = !0, e;
      };
    }, t.values = j, L.prototype = {
      constructor: L,
      reset: function (t) {
        if (this.prev = 0, this.next = 0, this.sent = this._sent = e, this.done = !1, this.delegate = null, this.method = "next", this.arg = e, this.tryEntries.forEach(A), !t) for (var n in this) "t" === n.charAt(0) && r.call(this, n) && !isNaN(+n.slice(1)) && (this[n] = e);
      },
      stop: function () {
        this.done = !0;
        var e = this.tryEntries[0].completion;
        if ("throw" === e.type) throw e.arg;
        return this.rval;
      },
      dispatchException: function (t) {
        if (this.done) throw t;
        var n = this;
        function i(r, i) {
          return s.type = "throw", s.arg = t, n.next = r, i && (n.method = "next", n.arg = e), !!i;
        }
        for (var o = this.tryEntries.length - 1; o >= 0; --o) {
          var a = this.tryEntries[o],
            s = a.completion;
          if ("root" === a.tryLoc) return i("end");
          if (a.tryLoc <= this.prev) {
            var u = r.call(a, "catchLoc"),
              c = r.call(a, "finallyLoc");
            if (u && c) {
              if (this.prev < a.catchLoc) return i(a.catchLoc, !0);
              if (this.prev < a.finallyLoc) return i(a.finallyLoc);
            } else if (u) {
              if (this.prev < a.catchLoc) return i(a.catchLoc, !0);
            } else {
              if (!c) throw Error("try statement without catch or finally");
              if (this.prev < a.finallyLoc) return i(a.finallyLoc);
            }
          }
        }
      },
      abrupt: function (e, t) {
        for (var n = this.tryEntries.length - 1; n >= 0; --n) {
          var i = this.tryEntries[n];
          if (i.tryLoc <= this.prev && r.call(i, "finallyLoc") && this.prev < i.finallyLoc) {
            var o = i;
            break;
          }
        }
        o && ("break" === e || "continue" === e) && o.tryLoc <= t && t <= o.finallyLoc && (o = null);
        var a = o ? o.completion : {};
        return a.type = e, a.arg = t, o ? (this.method = "next", this.next = o.finallyLoc, y) : this.complete(a);
      },
      complete: function (e, t) {
        if ("throw" === e.type) throw e.arg;
        return "break" === e.type || "continue" === e.type ? this.next = e.arg : "return" === e.type ? (this.rval = this.arg = e.arg, this.method = "return", this.next = "end") : "normal" === e.type && t && (this.next = t), y;
      },
      finish: function (e) {
        for (var t = this.tryEntries.length - 1; t >= 0; --t) {
          var n = this.tryEntries[t];
          if (n.finallyLoc === e) return this.complete(n.completion, n.afterLoc), A(n), y;
        }
      },
      catch: function (e) {
        for (var t = this.tryEntries.length - 1; t >= 0; --t) {
          var n = this.tryEntries[t];
          if (n.tryLoc === e) {
            var r = n.completion;
            if ("throw" === r.type) {
              var i = r.arg;
              A(n);
            }
            return i;
          }
        }
        throw Error("illegal catch attempt");
      },
      delegateYield: function (t, n, r) {
        return this.delegate = {
          iterator: j(t),
          resultName: n,
          nextLoc: r
        }, "next" === this.method && (this.arg = e), y;
      }
    }, t;
  }
  function u(e) {
    var t = function (e, t) {
      if ("object" != typeof e || !e) return e;
      var n = e[Symbol.toPrimitive];
      if (void 0 !== n) {
        var r = n.call(e, t || "default");
        if ("object" != typeof r) return r;
        throw new TypeError("@@toPrimitive must return a primitive value.");
      }
      return ("string" === t ? String : Number)(e);
    }(e, "string");
    return "symbol" == typeof t ? t : t + "";
  }
  function c(e, t, n, r, i, o, a) {
    try {
      var s = e[o](a),
        u = s.value;
    } catch (c) {
      return void n(c);
    }
    s.done ? t(u) : Promise.resolve(u).then(r, i);
  }
  function l(e) {
    return function () {
      var t = this,
        n = arguments;
      return new Promise(function (r, i) {
        var o = e.apply(t, n);
        function a(e) {
          c(o, r, i, a, s, "next", e);
        }
        function s(e) {
          c(o, r, i, a, s, "throw", e);
        }
        a(void 0);
      });
    };
  }
  function f(e, t) {
    if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
  }
  function h(e, t) {
    for (var n = 0; n < t.length; n++) {
      var r = t[n];
      r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(e, u(r.key), r);
    }
  }
  function d(e, t, n) {
    return t && h(e.prototype, t), n && h(e, n), Object.defineProperty(e, "prototype", {
      writable: !1
    }), e;
  }
  function p(e, t, n) {
    return (t = u(t)) in e ? Object.defineProperty(e, t, {
      value: n,
      enumerable: !0,
      configurable: !0,
      writable: !0
    }) : e[t] = n, e;
  }
  function g(e, t) {
    if ("function" != typeof t && null !== t) throw new TypeError("Super expression must either be null or a function");
    e.prototype = Object.create(t && t.prototype, {
      constructor: {
        value: e,
        writable: !0,
        configurable: !0
      }
    }), Object.defineProperty(e, "prototype", {
      writable: !1
    }), t && y(e, t);
  }
  function v(e) {
    return (v = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function (e) {
      return e.__proto__ || Object.getPrototypeOf(e);
    })(e);
  }
  function y(e, t) {
    return (y = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function (e, t) {
      return e.__proto__ = t, e;
    })(e, t);
  }
  function m(e) {
    var t = "function" == typeof Map ? new Map() : void 0;
    return m = function (e) {
      if (null === e || !function (e) {
        try {
          return -1 !== Function.toString.call(e).indexOf("[native code]");
        } catch (t) {
          return "function" == typeof e;
        }
      }(e)) return e;
      if ("function" != typeof e) throw new TypeError("Super expression must either be null or a function");
      if (void 0 !== t) {
        if (t.has(e)) return t.get(e);
        t.set(e, n);
      }
      function n() {
        return function (e, t, n) {
          if (i()) return Reflect.construct.apply(null, arguments);
          var r = [null];
          r.push.apply(r, t);
          var o = new (e.bind.apply(e, r))();
          return n && y(o, n.prototype), o;
        }(e, arguments, v(this).constructor);
      }
      return n.prototype = Object.create(e.prototype, {
        constructor: {
          value: n,
          enumerable: !1,
          writable: !0,
          configurable: !0
        }
      }), y(n, e);
    }, m(e);
  }
  function b() {
    return b = "undefined" != typeof Reflect && Reflect.get ? Reflect.get.bind() : function (e, t, n) {
      var r = function (e, t) {
        for (; !Object.prototype.hasOwnProperty.call(e, t) && null !== (e = v(e)););
        return e;
      }(e, t);
      if (r) {
        var i = Object.getOwnPropertyDescriptor(r, t);
        return i.get ? i.get.call(arguments.length < 3 ? e : n) : i.value;
      }
    }, b.apply(this, arguments);
  }
  function w(e, t) {
    return function (e) {
      if (Array.isArray(e)) return e;
    }(e) || function (e, t) {
      var n = null == e ? null : "undefined" != typeof Symbol && e[Symbol.iterator] || e["@@iterator"];
      if (null != n) {
        var r,
          i,
          o,
          a,
          s = [],
          u = !0,
          c = !1;
        try {
          if (o = (n = n.call(e)).next, 0 === t) {
            if (Object(n) !== n) return;
            u = !1;
          } else for (; !(u = (r = o.call(n)).done) && (s.push(r.value), s.length !== t); u = !0);
        } catch (l) {
          c = !0, i = l;
        } finally {
          try {
            if (!u && null != n.return && (a = n.return(), Object(a) !== a)) return;
          } finally {
            if (c) throw i;
          }
        }
        return s;
      }
    }(e, t) || P(e, t) || function () {
      throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
    }();
  }
  function k(e) {
    return function (e) {
      if (Array.isArray(e)) return x(e);
    }(e) || function (e) {
      if ("undefined" != typeof Symbol && null != e[Symbol.iterator] || null != e["@@iterator"]) return Array.from(e);
    }(e) || P(e) || function () {
      throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
    }();
  }
  function P(e, t) {
    if (e) {
      if ("string" == typeof e) return x(e, t);
      var n = Object.prototype.toString.call(e).slice(8, -1);
      return "Object" === n && e.constructor && (n = e.constructor.name), "Map" === n || "Set" === n ? Array.from(e) : "Arguments" === n || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? x(e, t) : void 0;
    }
  }
  function x(e, t) {
    (null == t || t > e.length) && (t = e.length);
    for (var n = 0, r = new Array(t); n < t; n++) r[n] = e[n];
    return r;
  }
  function S(e, t, n) {
    !function (e, t) {
      if (t.has(e)) throw new TypeError("Cannot initialize the same private elements twice on an object");
    }(e, t), t.set(e, n);
  }
  !function () {
    try {
      var e = "undefined" != typeof window ? window : "undefined" != typeof global ? global : "undefined" != typeof self ? self : {},
        t = new Error().stack;
      t && (e._sentryDebugIds = e._sentryDebugIds || {}, e._sentryDebugIds[t] = "9bd9df65-295d-4eb4-a27b-f95247bee20f", e._sentryDebugIdIdentifier = "sentry-dbid-9bd9df65-295d-4eb4-a27b-f95247bee20f");
    } catch (n) {}
  }(), ("undefined" != typeof window ? window : "undefined" != typeof global ? global : "undefined" != typeof self ? self : {}).SENTRY_RELEASE = {
    id: "payment-form-v1.141.0"
  };
  var C = "undefined" != typeof globalThis ? globalThis : "undefined" != typeof window ? window : "undefined" != typeof global ? global : "undefined" != typeof self ? self : {};
  function E(e) {
    return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
  }
  var T = function (e) {
      return e && e.Math === Math && e;
    },
    O = T("object" == typeof globalThis && globalThis) || T("object" == typeof window && window) || T("object" == typeof self && self) || T("object" == typeof C && C) || T("object" == typeof C && C) || function () {
      return this;
    }() || Function("return this")(),
    I = {},
    A = function (e) {
      try {
        return !!e();
      } catch (t) {
        return !0;
      }
    },
    L = !A(function () {
      return 7 !== Object.defineProperty({}, 1, {
        get: function () {
          return 7;
        }
      })[1];
    }),
    j = !A(function () {
      var e = function () {}.bind();
      return "function" != typeof e || e.hasOwnProperty("prototype");
    }),
    R = j,
    B = Function.prototype.call,
    _ = R ? B.bind(B) : function () {
      return B.apply(B, arguments);
    },
    N = {},
    F = {}.propertyIsEnumerable,
    M = Object.getOwnPropertyDescriptor,
    U = M && !F.call({
      1: 2
    }, 1);
  N.f = U ? function (e) {
    var t = M(this, e);
    return !!t && t.enumerable;
  } : F;
  var D,
    z,
    V = function (e, t) {
      return {
        enumerable: !(1 & e),
        configurable: !(2 & e),
        writable: !(4 & e),
        value: t
      };
    },
    q = j,
    $ = Function.prototype,
    G = $.call,
    H = q && $.bind.bind(G, G),
    W = q ? H : function (e) {
      return function () {
        return G.apply(e, arguments);
      };
    },
    J = W,
    Z = J({}.toString),
    X = J("".slice),
    Y = function (e) {
      return X(Z(e), 8, -1);
    },
    K = A,
    Q = Y,
    ee = Object,
    te = W("".split),
    ne = K(function () {
      return !ee("z").propertyIsEnumerable(0);
    }) ? function (e) {
      return "String" === Q(e) ? te(e, "") : ee(e);
    } : ee,
    re = function (e) {
      return null == e;
    },
    ie = re,
    oe = TypeError,
    ae = function (e) {
      if (ie(e)) throw new oe("Can't call method on " + e);
      return e;
    },
    se = ne,
    ue = ae,
    ce = function (e) {
      return se(ue(e));
    },
    le = "object" == typeof document && document.all,
    fe = void 0 === le && void 0 !== le ? function (e) {
      return "function" == typeof e || e === le;
    } : function (e) {
      return "function" == typeof e;
    },
    he = fe,
    de = function (e) {
      return "object" == typeof e ? null !== e : he(e);
    },
    pe = O,
    ge = fe,
    ve = function (e, t) {
      return arguments.length < 2 ? function (e) {
        return ge(e) ? e : void 0;
      }(pe[e]) : pe[e] && pe[e][t];
    },
    ye = W({}.isPrototypeOf),
    me = "undefined" != typeof navigator && String(navigator.userAgent) || "",
    be = O,
    we = me,
    ke = be.process,
    Pe = be.Deno,
    xe = ke && ke.versions || Pe && Pe.version,
    Se = xe && xe.v8;
  Se && (z = (D = Se.split("."))[0] > 0 && D[0] < 4 ? 1 : +(D[0] + D[1])), !z && we && (!(D = we.match(/Edge\/(\d+)/)) || D[1] >= 74) && (D = we.match(/Chrome\/(\d+)/)) && (z = +D[1]);
  var Ce = z,
    Ee = Ce,
    Te = A,
    Oe = O.String,
    Ie = !!Object.getOwnPropertySymbols && !Te(function () {
      var e = Symbol("symbol detection");
      return !Oe(e) || !(Object(e) instanceof Symbol) || !Symbol.sham && Ee && Ee < 41;
    }),
    Ae = Ie && !Symbol.sham && "symbol" == typeof Symbol.iterator,
    Le = ve,
    je = fe,
    Re = ye,
    Be = Object,
    _e = Ae ? function (e) {
      return "symbol" == typeof e;
    } : function (e) {
      var t = Le("Symbol");
      return je(t) && Re(t.prototype, Be(e));
    },
    Ne = String,
    Fe = function (e) {
      try {
        return Ne(e);
      } catch (t) {
        return "Object";
      }
    },
    Me = fe,
    Ue = Fe,
    De = TypeError,
    ze = function (e) {
      if (Me(e)) return e;
      throw new De(Ue(e) + " is not a function");
    },
    Ve = ze,
    qe = re,
    $e = function (e, t) {
      var n = e[t];
      return qe(n) ? void 0 : Ve(n);
    },
    Ge = _,
    He = fe,
    We = de,
    Je = TypeError,
    Ze = {
      exports: {}
    },
    Xe = O,
    Ye = Object.defineProperty,
    Ke = function (e, t) {
      try {
        Ye(Xe, e, {
          value: t,
          configurable: !0,
          writable: !0
        });
      } catch (n) {
        Xe[e] = t;
      }
      return t;
    },
    Qe = O,
    et = Ke,
    tt = "__core-js_shared__",
    nt = Ze.exports = Qe[tt] || et(tt, {});
  (nt.versions || (nt.versions = [])).push({
    version: "3.37.1",
    mode: "global",
    copyright: "© 2014-2024 Denis Pushkarev (zloirock.ru)",
    license: "https://github.com/zloirock/core-js/blob/v3.37.1/LICENSE",
    source: "https://github.com/zloirock/core-js"
  });
  var rt = Ze.exports,
    it = rt,
    ot = function (e, t) {
      return it[e] || (it[e] = t || {});
    },
    at = ae,
    st = Object,
    ut = function (e) {
      return st(at(e));
    },
    ct = ut,
    lt = W({}.hasOwnProperty),
    ft = Object.hasOwn || function (e, t) {
      return lt(ct(e), t);
    },
    ht = W,
    dt = 0,
    pt = Math.random(),
    gt = ht(1..toString),
    vt = function (e) {
      return "Symbol(" + (void 0 === e ? "" : e) + ")_" + gt(++dt + pt, 36);
    },
    yt = ot,
    mt = ft,
    bt = vt,
    wt = Ie,
    kt = Ae,
    Pt = O.Symbol,
    xt = yt("wks"),
    St = kt ? Pt.for || Pt : Pt && Pt.withoutSetter || bt,
    Ct = function (e) {
      return mt(xt, e) || (xt[e] = wt && mt(Pt, e) ? Pt[e] : St("Symbol." + e)), xt[e];
    },
    Et = _,
    Tt = de,
    Ot = _e,
    It = $e,
    At = function (e, t) {
      var n, r;
      if ("string" === t && He(n = e.toString) && !We(r = Ge(n, e))) return r;
      if (He(n = e.valueOf) && !We(r = Ge(n, e))) return r;
      if ("string" !== t && He(n = e.toString) && !We(r = Ge(n, e))) return r;
      throw new Je("Can't convert object to primitive value");
    },
    Lt = TypeError,
    jt = Ct("toPrimitive"),
    Rt = function (e, t) {
      if (!Tt(e) || Ot(e)) return e;
      var n,
        r = It(e, jt);
      if (r) {
        if (void 0 === t && (t = "default"), n = Et(r, e, t), !Tt(n) || Ot(n)) return n;
        throw new Lt("Can't convert object to primitive value");
      }
      return void 0 === t && (t = "number"), At(e, t);
    },
    Bt = Rt,
    _t = _e,
    Nt = function (e) {
      var t = Bt(e, "string");
      return _t(t) ? t : t + "";
    },
    Ft = de,
    Mt = O.document,
    Ut = Ft(Mt) && Ft(Mt.createElement),
    Dt = function (e) {
      return Ut ? Mt.createElement(e) : {};
    },
    zt = Dt,
    Vt = !L && !A(function () {
      return 7 !== Object.defineProperty(zt("div"), "a", {
        get: function () {
          return 7;
        }
      }).a;
    }),
    qt = L,
    $t = _,
    Gt = N,
    Ht = V,
    Wt = ce,
    Jt = Nt,
    Zt = ft,
    Xt = Vt,
    Yt = Object.getOwnPropertyDescriptor;
  I.f = qt ? Yt : function (e, t) {
    if (e = Wt(e), t = Jt(t), Xt) try {
      return Yt(e, t);
    } catch (n) {}
    if (Zt(e, t)) return Ht(!$t(Gt.f, e, t), e[t]);
  };
  var Kt = {},
    Qt = L && A(function () {
      return 42 !== Object.defineProperty(function () {}, "prototype", {
        value: 42,
        writable: !1
      }).prototype;
    }),
    en = de,
    tn = String,
    nn = TypeError,
    rn = function (e) {
      if (en(e)) return e;
      throw new nn(tn(e) + " is not an object");
    },
    on = L,
    an = Vt,
    sn = Qt,
    un = rn,
    cn = Nt,
    ln = TypeError,
    fn = Object.defineProperty,
    hn = Object.getOwnPropertyDescriptor,
    dn = "enumerable",
    pn = "configurable",
    gn = "writable";
  Kt.f = on ? sn ? function (e, t, n) {
    if (un(e), t = cn(t), un(n), "function" == typeof e && "prototype" === t && "value" in n && gn in n && !n[gn]) {
      var r = hn(e, t);
      r && r[gn] && (e[t] = n.value, n = {
        configurable: pn in n ? n[pn] : r[pn],
        enumerable: dn in n ? n[dn] : r[dn],
        writable: !1
      });
    }
    return fn(e, t, n);
  } : fn : function (e, t, n) {
    if (un(e), t = cn(t), un(n), an) try {
      return fn(e, t, n);
    } catch (r) {}
    if ("get" in n || "set" in n) throw new ln("Accessors not supported");
    return "value" in n && (e[t] = n.value), e;
  };
  var vn = Kt,
    yn = V,
    mn = L ? function (e, t, n) {
      return vn.f(e, t, yn(1, n));
    } : function (e, t, n) {
      return e[t] = n, e;
    },
    bn = {
      exports: {}
    },
    wn = L,
    kn = ft,
    Pn = Function.prototype,
    xn = wn && Object.getOwnPropertyDescriptor,
    Sn = kn(Pn, "name"),
    Cn = {
      EXISTS: Sn,
      PROPER: Sn && "something" === function () {}.name,
      CONFIGURABLE: Sn && (!wn || wn && xn(Pn, "name").configurable)
    },
    En = fe,
    Tn = rt,
    On = W(Function.toString);
  En(Tn.inspectSource) || (Tn.inspectSource = function (e) {
    return On(e);
  });
  var In,
    An,
    Ln,
    jn = Tn.inspectSource,
    Rn = fe,
    Bn = O.WeakMap,
    _n = Rn(Bn) && /native code/.test(String(Bn)),
    Nn = vt,
    Fn = ot("keys"),
    Mn = function (e) {
      return Fn[e] || (Fn[e] = Nn(e));
    },
    Un = {},
    Dn = _n,
    zn = O,
    Vn = de,
    qn = mn,
    $n = ft,
    Gn = rt,
    Hn = Mn,
    Wn = Un,
    Jn = "Object already initialized",
    Zn = zn.TypeError,
    Xn = zn.WeakMap;
  if (Dn || Gn.state) {
    var Yn = Gn.state || (Gn.state = new Xn());
    Yn.get = Yn.get, Yn.has = Yn.has, Yn.set = Yn.set, In = function (e, t) {
      if (Yn.has(e)) throw new Zn(Jn);
      return t.facade = e, Yn.set(e, t), t;
    }, An = function (e) {
      return Yn.get(e) || {};
    }, Ln = function (e) {
      return Yn.has(e);
    };
  } else {
    var Kn = Hn("state");
    Wn[Kn] = !0, In = function (e, t) {
      if ($n(e, Kn)) throw new Zn(Jn);
      return t.facade = e, qn(e, Kn, t), t;
    }, An = function (e) {
      return $n(e, Kn) ? e[Kn] : {};
    }, Ln = function (e) {
      return $n(e, Kn);
    };
  }
  var Qn = {
      set: In,
      get: An,
      has: Ln,
      enforce: function (e) {
        return Ln(e) ? An(e) : In(e, {});
      },
      getterFor: function (e) {
        return function (t) {
          var n;
          if (!Vn(t) || (n = An(t)).type !== e) throw new Zn("Incompatible receiver, " + e + " required");
          return n;
        };
      }
    },
    er = W,
    tr = A,
    nr = fe,
    rr = ft,
    ir = L,
    or = Cn.CONFIGURABLE,
    ar = jn,
    sr = Qn.enforce,
    ur = Qn.get,
    cr = String,
    lr = Object.defineProperty,
    fr = er("".slice),
    hr = er("".replace),
    dr = er([].join),
    pr = ir && !tr(function () {
      return 8 !== lr(function () {}, "length", {
        value: 8
      }).length;
    }),
    gr = String(String).split("String"),
    vr = bn.exports = function (e, t, n) {
      "Symbol(" === fr(cr(t), 0, 7) && (t = "[" + hr(cr(t), /^Symbol\(([^)]*)\).*$/, "$1") + "]"), n && n.getter && (t = "get " + t), n && n.setter && (t = "set " + t), (!rr(e, "name") || or && e.name !== t) && (ir ? lr(e, "name", {
        value: t,
        configurable: !0
      }) : e.name = t), pr && n && rr(n, "arity") && e.length !== n.arity && lr(e, "length", {
        value: n.arity
      });
      try {
        n && rr(n, "constructor") && n.constructor ? ir && lr(e, "prototype", {
          writable: !1
        }) : e.prototype && (e.prototype = void 0);
      } catch (i) {}
      var r = sr(e);
      return rr(r, "source") || (r.source = dr(gr, "string" == typeof t ? t : "")), e;
    };
  Function.prototype.toString = vr(function () {
    return nr(this) && ur(this).source || ar(this);
  }, "toString");
  var yr = bn.exports,
    mr = fe,
    br = Kt,
    wr = yr,
    kr = Ke,
    Pr = function (e, t, n, r) {
      r || (r = {});
      var i = r.enumerable,
        o = void 0 !== r.name ? r.name : t;
      if (mr(n) && wr(n, o, r), r.global) i ? e[t] = n : kr(t, n);else {
        try {
          r.unsafe ? e[t] && (i = !0) : delete e[t];
        } catch (a) {}
        i ? e[t] = n : br.f(e, t, {
          value: n,
          enumerable: !1,
          configurable: !r.nonConfigurable,
          writable: !r.nonWritable
        });
      }
      return e;
    },
    xr = {},
    Sr = Math.ceil,
    Cr = Math.floor,
    Er = Math.trunc || function (e) {
      var t = +e;
      return (t > 0 ? Cr : Sr)(t);
    },
    Tr = function (e) {
      var t = +e;
      return t != t || 0 === t ? 0 : Er(t);
    },
    Or = Tr,
    Ir = Math.max,
    Ar = Math.min,
    Lr = function (e, t) {
      var n = Or(e);
      return n < 0 ? Ir(n + t, 0) : Ar(n, t);
    },
    jr = Tr,
    Rr = Math.min,
    Br = function (e) {
      var t = jr(e);
      return t > 0 ? Rr(t, 9007199254740991) : 0;
    },
    _r = Br,
    Nr = function (e) {
      return _r(e.length);
    },
    Fr = ce,
    Mr = Lr,
    Ur = Nr,
    Dr = function (e) {
      return function (t, n, r) {
        var i = Fr(t),
          o = Ur(i);
        if (0 === o) return !e && -1;
        var a,
          s = Mr(r, o);
        if (e && n != n) {
          for (; o > s;) if ((a = i[s++]) != a) return !0;
        } else for (; o > s; s++) if ((e || s in i) && i[s] === n) return e || s || 0;
        return !e && -1;
      };
    },
    zr = {
      includes: Dr(!0),
      indexOf: Dr(!1)
    },
    Vr = ft,
    qr = ce,
    $r = zr.indexOf,
    Gr = Un,
    Hr = W([].push),
    Wr = function (e, t) {
      var n,
        r = qr(e),
        i = 0,
        o = [];
      for (n in r) !Vr(Gr, n) && Vr(r, n) && Hr(o, n);
      for (; t.length > i;) Vr(r, n = t[i++]) && (~$r(o, n) || Hr(o, n));
      return o;
    },
    Jr = ["constructor", "hasOwnProperty", "isPrototypeOf", "propertyIsEnumerable", "toLocaleString", "toString", "valueOf"],
    Zr = Wr,
    Xr = Jr.concat("length", "prototype");
  xr.f = Object.getOwnPropertyNames || function (e) {
    return Zr(e, Xr);
  };
  var Yr = {};
  Yr.f = Object.getOwnPropertySymbols;
  var Kr = ve,
    Qr = xr,
    ei = Yr,
    ti = rn,
    ni = W([].concat),
    ri = Kr("Reflect", "ownKeys") || function (e) {
      var t = Qr.f(ti(e)),
        n = ei.f;
      return n ? ni(t, n(e)) : t;
    },
    ii = ft,
    oi = ri,
    ai = I,
    si = Kt,
    ui = A,
    ci = fe,
    li = /#|\.prototype\./,
    fi = function (e, t) {
      var n = di[hi(e)];
      return n === gi || n !== pi && (ci(t) ? ui(t) : !!t);
    },
    hi = fi.normalize = function (e) {
      return String(e).replace(li, ".").toLowerCase();
    },
    di = fi.data = {},
    pi = fi.NATIVE = "N",
    gi = fi.POLYFILL = "P",
    vi = fi,
    yi = O,
    mi = I.f,
    bi = mn,
    wi = Pr,
    ki = Ke,
    Pi = function (e, t, n) {
      for (var r = oi(t), i = si.f, o = ai.f, a = 0; a < r.length; a++) {
        var s = r[a];
        ii(e, s) || n && ii(n, s) || i(e, s, o(t, s));
      }
    },
    xi = vi,
    Si = function (e, t) {
      var n,
        r,
        i,
        o,
        a,
        s = e.target,
        u = e.global,
        c = e.stat;
      if (n = u ? yi : c ? yi[s] || ki(s, {}) : yi[s] && yi[s].prototype) for (r in t) {
        if (o = t[r], i = e.dontCallGetSet ? (a = mi(n, r)) && a.value : n[r], !xi(u ? r : s + (c ? "." : "#") + r, e.forced) && void 0 !== i) {
          if (typeof o == typeof i) continue;
          Pi(o, i);
        }
        (e.sham || i && i.sham) && bi(o, "sham", !0), wi(n, r, o, e);
      }
    },
    Ci = Y,
    Ei = Array.isArray || function (e) {
      return "Array" === Ci(e);
    },
    Ti = TypeError,
    Oi = L,
    Ii = Kt,
    Ai = V,
    Li = function (e, t, n) {
      Oi ? Ii.f(e, t, Ai(0, n)) : e[t] = n;
    },
    ji = {};
  ji[Ct("toStringTag")] = "z";
  var Ri = "[object z]" === String(ji),
    Bi = Ri,
    _i = fe,
    Ni = Y,
    Fi = Ct("toStringTag"),
    Mi = Object,
    Ui = "Arguments" === Ni(function () {
      return arguments;
    }()),
    Di = Bi ? Ni : function (e) {
      var t, n, r;
      return void 0 === e ? "Undefined" : null === e ? "Null" : "string" == typeof (n = function (e, t) {
        try {
          return e[t];
        } catch (n) {}
      }(t = Mi(e), Fi)) ? n : Ui ? Ni(t) : "Object" === (r = Ni(t)) && _i(t.callee) ? "Arguments" : r;
    },
    zi = W,
    Vi = A,
    qi = fe,
    $i = Di,
    Gi = jn,
    Hi = function () {},
    Wi = ve("Reflect", "construct"),
    Ji = /^\s*(?:class|function)\b/,
    Zi = zi(Ji.exec),
    Xi = !Ji.test(Hi),
    Yi = function (e) {
      if (!qi(e)) return !1;
      try {
        return Wi(Hi, [], e), !0;
      } catch (t) {
        return !1;
      }
    },
    Ki = function (e) {
      if (!qi(e)) return !1;
      switch ($i(e)) {
        case "AsyncFunction":
        case "GeneratorFunction":
        case "AsyncGeneratorFunction":
          return !1;
      }
      try {
        return Xi || !!Zi(Ji, Gi(e));
      } catch (t) {
        return !0;
      }
    };
  Ki.sham = !0;
  var Qi = !Wi || Vi(function () {
      var e;
      return Yi(Yi.call) || !Yi(Object) || !Yi(function () {
        e = !0;
      }) || e;
    }) ? Ki : Yi,
    eo = Ei,
    to = Qi,
    no = de,
    ro = Ct("species"),
    io = Array,
    oo = function (e) {
      var t;
      return eo(e) && (t = e.constructor, (to(t) && (t === io || eo(t.prototype)) || no(t) && null === (t = t[ro])) && (t = void 0)), void 0 === t ? io : t;
    },
    ao = function (e, t) {
      return new (oo(e))(0 === t ? 0 : t);
    },
    so = A,
    uo = Ce,
    co = Ct("species"),
    lo = function (e) {
      return uo >= 51 || !so(function () {
        var t = [];
        return (t.constructor = {})[co] = function () {
          return {
            foo: 1
          };
        }, 1 !== t[e](Boolean).foo;
      });
    },
    fo = Si,
    ho = A,
    po = Ei,
    go = de,
    vo = ut,
    yo = Nr,
    mo = function (e) {
      if (e > 9007199254740991) throw Ti("Maximum allowed index exceeded");
      return e;
    },
    bo = Li,
    wo = ao,
    ko = lo,
    Po = Ce,
    xo = Ct("isConcatSpreadable"),
    So = Po >= 51 || !ho(function () {
      var e = [];
      return e[xo] = !1, e.concat()[0] !== e;
    }),
    Co = function (e) {
      if (!go(e)) return !1;
      var t = e[xo];
      return void 0 !== t ? !!t : po(e);
    };
  fo({
    target: "Array",
    proto: !0,
    arity: 1,
    forced: !So || !ko("concat")
  }, {
    concat: function (e) {
      var t,
        n,
        r,
        i,
        o,
        a = vo(this),
        s = wo(a, 0),
        u = 0;
      for (t = -1, r = arguments.length; t < r; t++) if (Co(o = -1 === t ? a : arguments[t])) for (i = yo(o), mo(u + i), n = 0; n < i; n++, u++) n in o && bo(s, u, o[n]);else mo(u + 1), bo(s, u++, o);
      return s.length = u, s;
    }
  });
  var Eo = Di,
    To = Ri ? {}.toString : function () {
      return "[object " + Eo(this) + "]";
    };
  Ri || Pr(Object.prototype, "toString", To, {
    unsafe: !0
  });
  var Oo,
    Io,
    Ao,
    Lo,
    jo = "process" === Y(O.process),
    Ro = W,
    Bo = ze,
    _o = de,
    No = function (e) {
      return _o(e) || null === e;
    },
    Fo = String,
    Mo = TypeError,
    Uo = function (e, t, n) {
      try {
        return Ro(Bo(Object.getOwnPropertyDescriptor(e, t)[n]));
      } catch (r) {}
    },
    Do = de,
    zo = ae,
    Vo = function (e) {
      if (No(e)) return e;
      throw new Mo("Can't set " + Fo(e) + " as a prototype");
    },
    qo = Object.setPrototypeOf || ("__proto__" in {} ? function () {
      var e,
        t = !1,
        n = {};
      try {
        (e = Uo(Object.prototype, "__proto__", "set"))(n, []), t = n instanceof Array;
      } catch (r) {}
      return function (n, r) {
        return zo(n), Vo(r), Do(n) ? (t ? e(n, r) : n.__proto__ = r, n) : n;
      };
    }() : void 0),
    $o = Kt.f,
    Go = ft,
    Ho = Ct("toStringTag"),
    Wo = function (e, t, n) {
      e && !n && (e = e.prototype), e && !Go(e, Ho) && $o(e, Ho, {
        configurable: !0,
        value: t
      });
    },
    Jo = yr,
    Zo = Kt,
    Xo = function (e, t, n) {
      return n.get && Jo(n.get, t, {
        getter: !0
      }), n.set && Jo(n.set, t, {
        setter: !0
      }), Zo.f(e, t, n);
    },
    Yo = ve,
    Ko = Xo,
    Qo = L,
    ea = Ct("species"),
    ta = function (e) {
      var t = Yo(e);
      Qo && t && !t[ea] && Ko(t, ea, {
        configurable: !0,
        get: function () {
          return this;
        }
      });
    },
    na = ye,
    ra = TypeError,
    ia = function (e, t) {
      if (na(t, e)) return e;
      throw new ra("Incorrect invocation");
    },
    oa = Qi,
    aa = Fe,
    sa = TypeError,
    ua = rn,
    ca = function (e) {
      if (oa(e)) return e;
      throw new sa(aa(e) + " is not a constructor");
    },
    la = re,
    fa = Ct("species"),
    ha = j,
    da = Function.prototype,
    pa = da.apply,
    ga = da.call,
    va = "object" == typeof Reflect && Reflect.apply || (ha ? ga.bind(pa) : function () {
      return ga.apply(pa, arguments);
    }),
    ya = Y,
    ma = W,
    ba = function (e) {
      if ("Function" === ya(e)) return ma(e);
    },
    wa = ze,
    ka = j,
    Pa = ba(ba.bind),
    xa = function (e, t) {
      return wa(e), void 0 === t ? e : ka ? Pa(e, t) : function () {
        return e.apply(t, arguments);
      };
    },
    Sa = ve("document", "documentElement"),
    Ca = W([].slice),
    Ea = TypeError,
    Ta = function (e, t) {
      if (e < t) throw new Ea("Not enough arguments");
      return e;
    },
    Oa = /(?:ipad|iphone|ipod).*applewebkit/i.test(me),
    Ia = O,
    Aa = va,
    La = xa,
    ja = fe,
    Ra = ft,
    Ba = A,
    _a = Sa,
    Na = Ca,
    Fa = Dt,
    Ma = Ta,
    Ua = Oa,
    Da = jo,
    za = Ia.setImmediate,
    Va = Ia.clearImmediate,
    qa = Ia.process,
    $a = Ia.Dispatch,
    Ga = Ia.Function,
    Ha = Ia.MessageChannel,
    Wa = Ia.String,
    Ja = 0,
    Za = {},
    Xa = "onreadystatechange";
  Ba(function () {
    Oo = Ia.location;
  });
  var Ya = function (e) {
      if (Ra(Za, e)) {
        var t = Za[e];
        delete Za[e], t();
      }
    },
    Ka = function (e) {
      return function () {
        Ya(e);
      };
    },
    Qa = function (e) {
      Ya(e.data);
    },
    es = function (e) {
      Ia.postMessage(Wa(e), Oo.protocol + "//" + Oo.host);
    };
  za && Va || (za = function (e) {
    Ma(arguments.length, 1);
    var t = ja(e) ? e : Ga(e),
      n = Na(arguments, 1);
    return Za[++Ja] = function () {
      Aa(t, void 0, n);
    }, Io(Ja), Ja;
  }, Va = function (e) {
    delete Za[e];
  }, Da ? Io = function (e) {
    qa.nextTick(Ka(e));
  } : $a && $a.now ? Io = function (e) {
    $a.now(Ka(e));
  } : Ha && !Ua ? (Lo = (Ao = new Ha()).port2, Ao.port1.onmessage = Qa, Io = La(Lo.postMessage, Lo)) : Ia.addEventListener && ja(Ia.postMessage) && !Ia.importScripts && Oo && "file:" !== Oo.protocol && !Ba(es) ? (Io = es, Ia.addEventListener("message", Qa, !1)) : Io = Xa in Fa("script") ? function (e) {
    _a.appendChild(Fa("script"))[Xa] = function () {
      _a.removeChild(this), Ya(e);
    };
  } : function (e) {
    setTimeout(Ka(e), 0);
  });
  var ts = {
      set: za,
      clear: Va
    },
    ns = O,
    rs = L,
    is = Object.getOwnPropertyDescriptor,
    os = function (e) {
      if (!rs) return ns[e];
      var t = is(ns, e);
      return t && t.value;
    },
    as = function () {
      this.head = null, this.tail = null;
    };
  as.prototype = {
    add: function (e) {
      var t = {
          item: e,
          next: null
        },
        n = this.tail;
      n ? n.next = t : this.head = t, this.tail = t;
    },
    get: function () {
      var e = this.head;
      if (e) return null === (this.head = e.next) && (this.tail = null), e.item;
    }
  };
  var ss,
    us,
    cs,
    ls,
    fs,
    hs = as,
    ds = /ipad|iphone|ipod/i.test(me) && "undefined" != typeof Pebble,
    ps = /web0s(?!.*chrome)/i.test(me),
    gs = O,
    vs = os,
    ys = xa,
    ms = ts.set,
    bs = hs,
    ws = Oa,
    ks = ds,
    Ps = ps,
    xs = jo,
    Ss = gs.MutationObserver || gs.WebKitMutationObserver,
    Cs = gs.document,
    Es = gs.process,
    Ts = gs.Promise,
    Os = vs("queueMicrotask");
  if (!Os) {
    var Is = new bs(),
      As = function () {
        var e, t;
        for (xs && (e = Es.domain) && e.exit(); t = Is.get();) try {
          t();
        } catch (n) {
          throw Is.head && ss(), n;
        }
        e && e.enter();
      };
    ws || xs || Ps || !Ss || !Cs ? !ks && Ts && Ts.resolve ? ((ls = Ts.resolve(void 0)).constructor = Ts, fs = ys(ls.then, ls), ss = function () {
      fs(As);
    }) : xs ? ss = function () {
      Es.nextTick(As);
    } : (ms = ys(ms, gs), ss = function () {
      ms(As);
    }) : (us = !0, cs = Cs.createTextNode(""), new Ss(As).observe(cs, {
      characterData: !0
    }), ss = function () {
      cs.data = us = !us;
    }), Os = function (e) {
      Is.head || ss(), Is.add(e);
    };
  }
  var Ls = Os,
    js = function (e) {
      try {
        return {
          error: !1,
          value: e()
        };
      } catch (t) {
        return {
          error: !0,
          value: t
        };
      }
    },
    Rs = O.Promise,
    Bs = "object" == typeof Deno && Deno && "object" == typeof Deno.version,
    _s = !Bs && !jo && "object" == typeof window && "object" == typeof document,
    Ns = O,
    Fs = Rs,
    Ms = fe,
    Us = vi,
    Ds = jn,
    zs = Ct,
    Vs = _s,
    qs = Bs,
    $s = Ce;
  Fs && Fs.prototype;
  var Gs = zs("species"),
    Hs = !1,
    Ws = Ms(Ns.PromiseRejectionEvent),
    Js = {
      CONSTRUCTOR: Us("Promise", function () {
        var e = Ds(Fs),
          t = e !== String(Fs);
        if (!t && 66 === $s) return !0;
        if (!$s || $s < 51 || !/native code/.test(e)) {
          var n = new Fs(function (e) {
              e(1);
            }),
            r = function (e) {
              e(function () {}, function () {});
            };
          if ((n.constructor = {})[Gs] = r, !(Hs = n.then(function () {}) instanceof r)) return !0;
        }
        return !t && (Vs || qs) && !Ws;
      }),
      REJECTION_EVENT: Ws,
      SUBCLASSING: Hs
    },
    Zs = {},
    Xs = ze,
    Ys = TypeError,
    Ks = function (e) {
      var t, n;
      this.promise = new e(function (e, r) {
        if (void 0 !== t || void 0 !== n) throw new Ys("Bad Promise constructor");
        t = e, n = r;
      }), this.resolve = Xs(t), this.reject = Xs(n);
    };
  Zs.f = function (e) {
    return new Ks(e);
  };
  var Qs,
    eu,
    tu,
    nu = Si,
    ru = jo,
    iu = O,
    ou = _,
    au = Pr,
    su = qo,
    uu = Wo,
    cu = ta,
    lu = ze,
    fu = fe,
    hu = de,
    du = ia,
    pu = function (e, t) {
      var n,
        r = ua(e).constructor;
      return void 0 === r || la(n = ua(r)[fa]) ? t : ca(n);
    },
    gu = ts.set,
    vu = Ls,
    yu = function (e, t) {
      try {
        1 === arguments.length ? console.error(e) : console.error(e, t);
      } catch (n) {}
    },
    mu = js,
    bu = hs,
    wu = Qn,
    ku = Rs,
    Pu = Zs,
    xu = "Promise",
    Su = Js.CONSTRUCTOR,
    Cu = Js.REJECTION_EVENT,
    Eu = Js.SUBCLASSING,
    Tu = wu.getterFor(xu),
    Ou = wu.set,
    Iu = ku && ku.prototype,
    Au = ku,
    Lu = Iu,
    ju = iu.TypeError,
    Ru = iu.document,
    Bu = iu.process,
    _u = Pu.f,
    Nu = _u,
    Fu = !!(Ru && Ru.createEvent && iu.dispatchEvent),
    Mu = "unhandledrejection",
    Uu = function (e) {
      var t;
      return !(!hu(e) || !fu(t = e.then)) && t;
    },
    Du = function (e, t) {
      var n,
        r,
        i,
        o = t.value,
        a = 1 === t.state,
        s = a ? e.ok : e.fail,
        u = e.resolve,
        c = e.reject,
        l = e.domain;
      try {
        s ? (a || (2 === t.rejection && Gu(t), t.rejection = 1), !0 === s ? n = o : (l && l.enter(), n = s(o), l && (l.exit(), i = !0)), n === e.promise ? c(new ju("Promise-chain cycle")) : (r = Uu(n)) ? ou(r, n, u, c) : u(n)) : c(o);
      } catch (f) {
        l && !i && l.exit(), c(f);
      }
    },
    zu = function (e, t) {
      e.notified || (e.notified = !0, vu(function () {
        for (var n, r = e.reactions; n = r.get();) Du(n, e);
        e.notified = !1, t && !e.rejection && qu(e);
      }));
    },
    Vu = function (e, t, n) {
      var r, i;
      Fu ? ((r = Ru.createEvent("Event")).promise = t, r.reason = n, r.initEvent(e, !1, !0), iu.dispatchEvent(r)) : r = {
        promise: t,
        reason: n
      }, !Cu && (i = iu["on" + e]) ? i(r) : e === Mu && yu("Unhandled promise rejection", n);
    },
    qu = function (e) {
      ou(gu, iu, function () {
        var t,
          n = e.facade,
          r = e.value;
        if ($u(e) && (t = mu(function () {
          ru ? Bu.emit("unhandledRejection", r, n) : Vu(Mu, n, r);
        }), e.rejection = ru || $u(e) ? 2 : 1, t.error)) throw t.value;
      });
    },
    $u = function (e) {
      return 1 !== e.rejection && !e.parent;
    },
    Gu = function (e) {
      ou(gu, iu, function () {
        var t = e.facade;
        ru ? Bu.emit("rejectionHandled", t) : Vu("rejectionhandled", t, e.value);
      });
    },
    Hu = function (e, t, n) {
      return function (r) {
        e(t, r, n);
      };
    },
    Wu = function (e, t, n) {
      e.done || (e.done = !0, n && (e = n), e.value = t, e.state = 2, zu(e, !0));
    },
    Ju = function (e, t, n) {
      if (!e.done) {
        e.done = !0, n && (e = n);
        try {
          if (e.facade === t) throw new ju("Promise can't be resolved itself");
          var r = Uu(t);
          r ? vu(function () {
            var n = {
              done: !1
            };
            try {
              ou(r, t, Hu(Ju, n, e), Hu(Wu, n, e));
            } catch (i) {
              Wu(n, i, e);
            }
          }) : (e.value = t, e.state = 1, zu(e, !1));
        } catch (i) {
          Wu({
            done: !1
          }, i, e);
        }
      }
    };
  if (Su && (Lu = (Au = function (e) {
    du(this, Lu), lu(e), ou(Qs, this);
    var t = Tu(this);
    try {
      e(Hu(Ju, t), Hu(Wu, t));
    } catch (n) {
      Wu(t, n);
    }
  }).prototype, (Qs = function (e) {
    Ou(this, {
      type: xu,
      done: !1,
      notified: !1,
      parent: !1,
      reactions: new bu(),
      rejection: !1,
      state: 0,
      value: void 0
    });
  }).prototype = au(Lu, "then", function (e, t) {
    var n = Tu(this),
      r = _u(pu(this, Au));
    return n.parent = !0, r.ok = !fu(e) || e, r.fail = fu(t) && t, r.domain = ru ? Bu.domain : void 0, 0 === n.state ? n.reactions.add(r) : vu(function () {
      Du(r, n);
    }), r.promise;
  }), eu = function () {
    var e = new Qs(),
      t = Tu(e);
    this.promise = e, this.resolve = Hu(Ju, t), this.reject = Hu(Wu, t);
  }, Pu.f = _u = function (e) {
    return e === Au || undefined === e ? new eu(e) : Nu(e);
  }, fu(ku) && Iu !== Object.prototype)) {
    tu = Iu.then, Eu || au(Iu, "then", function (e, t) {
      var n = this;
      return new Au(function (e, t) {
        ou(tu, n, e, t);
      }).then(e, t);
    }, {
      unsafe: !0
    });
    try {
      delete Iu.constructor;
    } catch (UO) {}
    su && su(Iu, Lu);
  }
  nu({
    global: !0,
    constructor: !0,
    wrap: !0,
    forced: Su
  }, {
    Promise: Au
  }), uu(Au, xu, !1), cu(xu);
  var Zu = {},
    Xu = Zu,
    Yu = Ct("iterator"),
    Ku = Array.prototype,
    Qu = function (e) {
      return void 0 !== e && (Xu.Array === e || Ku[Yu] === e);
    },
    ec = Di,
    tc = $e,
    nc = re,
    rc = Zu,
    ic = Ct("iterator"),
    oc = function (e) {
      if (!nc(e)) return tc(e, ic) || tc(e, "@@iterator") || rc[ec(e)];
    },
    ac = _,
    sc = ze,
    uc = rn,
    cc = Fe,
    lc = oc,
    fc = TypeError,
    hc = function (e, t) {
      var n = arguments.length < 2 ? lc(e) : t;
      if (sc(n)) return uc(ac(n, e));
      throw new fc(cc(e) + " is not iterable");
    },
    dc = _,
    pc = rn,
    gc = $e,
    vc = function (e, t, n) {
      var r, i;
      pc(e);
      try {
        if (!(r = gc(e, "return"))) {
          if ("throw" === t) throw n;
          return n;
        }
        r = dc(r, e);
      } catch (UO) {
        i = !0, r = UO;
      }
      if ("throw" === t) throw n;
      if (i) throw r;
      return pc(r), n;
    },
    yc = xa,
    mc = _,
    bc = rn,
    wc = Fe,
    kc = Qu,
    Pc = Nr,
    xc = ye,
    Sc = hc,
    Cc = oc,
    Ec = vc,
    Tc = TypeError,
    Oc = function (e, t) {
      this.stopped = e, this.result = t;
    },
    Ic = Oc.prototype,
    Ac = function (e, t, n) {
      var r,
        i,
        o,
        a,
        s,
        u,
        c,
        l = n && n.that,
        f = !(!n || !n.AS_ENTRIES),
        h = !(!n || !n.IS_RECORD),
        d = !(!n || !n.IS_ITERATOR),
        p = !(!n || !n.INTERRUPTED),
        g = yc(t, l),
        v = function (e) {
          return r && Ec(r, "normal", e), new Oc(!0, e);
        },
        y = function (e) {
          return f ? (bc(e), p ? g(e[0], e[1], v) : g(e[0], e[1])) : p ? g(e, v) : g(e);
        };
      if (h) r = e.iterator;else if (d) r = e;else {
        if (!(i = Cc(e))) throw new Tc(wc(e) + " is not iterable");
        if (kc(i)) {
          for (o = 0, a = Pc(e); a > o; o++) if ((s = y(e[o])) && xc(Ic, s)) return s;
          return new Oc(!1);
        }
        r = Sc(e, i);
      }
      for (u = h ? e.next : r.next; !(c = mc(u, r)).done;) {
        try {
          s = y(c.value);
        } catch (UO) {
          Ec(r, "throw", UO);
        }
        if ("object" == typeof s && s && xc(Ic, s)) return s;
      }
      return new Oc(!1);
    },
    Lc = Ct("iterator"),
    jc = !1;
  try {
    var Rc = 0,
      Bc = {
        next: function () {
          return {
            done: !!Rc++
          };
        },
        return: function () {
          jc = !0;
        }
      };
    Bc[Lc] = function () {
      return this;
    }, Array.from(Bc, function () {
      throw 2;
    });
  } catch (UO) {}
  var _c = function (e, t) {
      try {
        if (!t && !jc) return !1;
      } catch (UO) {
        return !1;
      }
      var n = !1;
      try {
        var r = {};
        r[Lc] = function () {
          return {
            next: function () {
              return {
                done: n = !0
              };
            }
          };
        }, e(r);
      } catch (UO) {}
      return n;
    },
    Nc = Rs,
    Fc = Js.CONSTRUCTOR || !_c(function (e) {
      Nc.all(e).then(void 0, function () {});
    }),
    Mc = _,
    Uc = ze,
    Dc = Zs,
    zc = js,
    Vc = Ac;
  Si({
    target: "Promise",
    stat: !0,
    forced: Fc
  }, {
    all: function (e) {
      var t = this,
        n = Dc.f(t),
        r = n.resolve,
        i = n.reject,
        o = zc(function () {
          var n = Uc(t.resolve),
            o = [],
            a = 0,
            s = 1;
          Vc(e, function (e) {
            var u = a++,
              c = !1;
            s++, Mc(n, t, e).then(function (e) {
              c || (c = !0, o[u] = e, --s || r(o));
            }, i);
          }), --s || r(o);
        });
      return o.error && i(o.value), n.promise;
    }
  });
  var qc = Si,
    $c = Js.CONSTRUCTOR,
    Gc = Rs,
    Hc = ve,
    Wc = fe,
    Jc = Pr,
    Zc = Gc && Gc.prototype;
  if (qc({
    target: "Promise",
    proto: !0,
    forced: $c,
    real: !0
  }, {
    catch: function (e) {
      return this.then(void 0, e);
    }
  }), Wc(Gc)) {
    var Xc = Hc("Promise").prototype.catch;
    Zc.catch !== Xc && Jc(Zc, "catch", Xc, {
      unsafe: !0
    });
  }
  var Yc = _,
    Kc = ze,
    Qc = Zs,
    el = js,
    tl = Ac;
  Si({
    target: "Promise",
    stat: !0,
    forced: Fc
  }, {
    race: function (e) {
      var t = this,
        n = Qc.f(t),
        r = n.reject,
        i = el(function () {
          var i = Kc(t.resolve);
          tl(e, function (e) {
            Yc(i, t, e).then(n.resolve, r);
          });
        });
      return i.error && r(i.value), n.promise;
    }
  });
  var nl = Zs;
  Si({
    target: "Promise",
    stat: !0,
    forced: Js.CONSTRUCTOR
  }, {
    reject: function (e) {
      var t = nl.f(this);
      return (0, t.reject)(e), t.promise;
    }
  });
  var rl = rn,
    il = de,
    ol = Zs,
    al = Si,
    sl = Js.CONSTRUCTOR,
    ul = function (e, t) {
      if (rl(e), il(t) && t.constructor === e) return t;
      var n = ol.f(e);
      return (0, n.resolve)(t), n.promise;
    };
  ve("Promise"), al({
    target: "Promise",
    stat: !0,
    forced: sl
  }, {
    resolve: function (e) {
      return ul(this, e);
    }
  });
  var cl = {},
    ll = Wr,
    fl = Jr,
    hl = Object.keys || function (e) {
      return ll(e, fl);
    },
    dl = L,
    pl = Qt,
    gl = Kt,
    vl = rn,
    yl = ce,
    ml = hl;
  cl.f = dl && !pl ? Object.defineProperties : function (e, t) {
    vl(e);
    for (var n, r = yl(t), i = ml(t), o = i.length, a = 0; o > a;) gl.f(e, n = i[a++], r[n]);
    return e;
  };
  var bl,
    wl = rn,
    kl = cl,
    Pl = Jr,
    xl = Un,
    Sl = Sa,
    Cl = Dt,
    El = "prototype",
    Tl = "script",
    Ol = Mn("IE_PROTO"),
    Il = function () {},
    Al = function (e) {
      return "<" + Tl + ">" + e + "</" + Tl + ">";
    },
    Ll = function (e) {
      e.write(Al("")), e.close();
      var t = e.parentWindow.Object;
      return e = null, t;
    },
    jl = function () {
      try {
        bl = new ActiveXObject("htmlfile");
      } catch (UO) {}
      jl = "undefined" != typeof document ? document.domain && bl ? Ll(bl) : function () {
        var e,
          t = Cl("iframe"),
          n = "java" + Tl + ":";
        return t.style.display = "none", Sl.appendChild(t), t.src = String(n), (e = t.contentWindow.document).open(), e.write(Al("document.F=Object")), e.close(), e.F;
      }() : Ll(bl);
      for (var e = Pl.length; e--;) delete jl[El][Pl[e]];
      return jl();
    };
  xl[Ol] = !0;
  var Rl = Object.create || function (e, t) {
      var n;
      return null !== e ? (Il[El] = wl(e), n = new Il(), Il[El] = null, n[Ol] = e) : n = jl(), void 0 === t ? n : kl.f(n, t);
    },
    Bl = Ct,
    _l = Rl,
    Nl = Kt.f,
    Fl = Bl("unscopables"),
    Ml = Array.prototype;
  void 0 === Ml[Fl] && Nl(Ml, Fl, {
    configurable: !0,
    value: _l(null)
  });
  var Ul = function (e) {
      Ml[Fl][e] = !0;
    },
    Dl = zr.includes,
    zl = Ul;
  Si({
    target: "Array",
    proto: !0,
    forced: A(function () {
      return !Array(1).includes();
    })
  }, {
    includes: function (e) {
      return Dl(this, e, arguments.length > 1 ? arguments[1] : void 0);
    }
  }), zl("includes");
  var Vl,
    ql,
    $l,
    Gl = !A(function () {
      function e() {}
      return e.prototype.constructor = null, Object.getPrototypeOf(new e()) !== e.prototype;
    }),
    Hl = ft,
    Wl = fe,
    Jl = ut,
    Zl = Gl,
    Xl = Mn("IE_PROTO"),
    Yl = Object,
    Kl = Yl.prototype,
    Ql = Zl ? Yl.getPrototypeOf : function (e) {
      var t = Jl(e);
      if (Hl(t, Xl)) return t[Xl];
      var n = t.constructor;
      return Wl(n) && t instanceof n ? n.prototype : t instanceof Yl ? Kl : null;
    },
    ef = A,
    tf = fe,
    nf = de,
    rf = Ql,
    of = Pr,
    af = Ct("iterator"),
    sf = !1;
  [].keys && ("next" in ($l = [].keys()) ? (ql = rf(rf($l))) !== Object.prototype && (Vl = ql) : sf = !0), (!nf(Vl) || ef(function () {
    var e = {};
    return Vl[af].call(e) !== e;
  })) && (Vl = {}), tf(Vl[af]) || of(Vl, af, function () {
    return this;
  });
  var uf = {
      IteratorPrototype: Vl,
      BUGGY_SAFARI_ITERATORS: sf
    },
    cf = uf.IteratorPrototype,
    lf = Rl,
    ff = V,
    hf = Wo,
    df = Zu,
    pf = function () {
      return this;
    },
    gf = function (e, t, n, r) {
      var i = t + " Iterator";
      return e.prototype = lf(cf, {
        next: ff(+!r, n)
      }), hf(e, i, !1), df[i] = pf, e;
    },
    vf = Si,
    yf = _,
    mf = fe,
    bf = gf,
    wf = Ql,
    kf = qo,
    Pf = Wo,
    xf = mn,
    Sf = Pr,
    Cf = Zu,
    Ef = Cn.PROPER,
    Tf = Cn.CONFIGURABLE,
    Of = uf.IteratorPrototype,
    If = uf.BUGGY_SAFARI_ITERATORS,
    Af = Ct("iterator"),
    Lf = "keys",
    jf = "values",
    Rf = "entries",
    Bf = function () {
      return this;
    },
    _f = function (e, t, n, r, i, o, a) {
      bf(n, t, r);
      var s,
        u,
        c,
        l = function (e) {
          if (e === i && g) return g;
          if (!If && e && e in d) return d[e];
          switch (e) {
            case Lf:
            case jf:
            case Rf:
              return function () {
                return new n(this, e);
              };
          }
          return function () {
            return new n(this);
          };
        },
        f = t + " Iterator",
        h = !1,
        d = e.prototype,
        p = d[Af] || d["@@iterator"] || i && d[i],
        g = !If && p || l(i),
        v = "Array" === t && d.entries || p;
      if (v && (s = wf(v.call(new e()))) !== Object.prototype && s.next && (wf(s) !== Of && (kf ? kf(s, Of) : mf(s[Af]) || Sf(s, Af, Bf)), Pf(s, f, !0)), Ef && i === jf && p && p.name !== jf && (Tf ? xf(d, "name", jf) : (h = !0, g = function () {
        return yf(p, this);
      })), i) if (u = {
        values: l(jf),
        keys: o ? g : l(Lf),
        entries: l(Rf)
      }, a) for (c in u) (If || h || !(c in d)) && Sf(d, c, u[c]);else vf({
        target: t,
        proto: !0,
        forced: If || h
      }, u);
      return d[Af] !== g && Sf(d, Af, g, {
        name: i
      }), Cf[t] = g, u;
    },
    Nf = function (e, t) {
      return {
        value: e,
        done: t
      };
    },
    Ff = ce,
    Mf = Ul,
    Uf = Zu,
    Df = Qn,
    zf = Kt.f,
    Vf = _f,
    qf = Nf,
    $f = L,
    Gf = "Array Iterator",
    Hf = Df.set,
    Wf = Df.getterFor(Gf),
    Jf = Vf(Array, "Array", function (e, t) {
      Hf(this, {
        type: Gf,
        target: Ff(e),
        index: 0,
        kind: t
      });
    }, function () {
      var e = Wf(this),
        t = e.target,
        n = e.index++;
      if (!t || n >= t.length) return e.target = void 0, qf(void 0, !0);
      switch (e.kind) {
        case "keys":
          return qf(n, !1);
        case "values":
          return qf(t[n], !1);
      }
      return qf([n, t[n]], !1);
    }, "values"),
    Zf = Uf.Arguments = Uf.Array;
  if (Mf("keys"), Mf("values"), Mf("entries"), $f && "values" !== Zf.name) try {
    zf(Zf, "name", {
      value: "values"
    });
  } catch (UO) {}
  var Xf = Di,
    Yf = String,
    Kf = function (e) {
      if ("Symbol" === Xf(e)) throw new TypeError("Cannot convert a Symbol value to a string");
      return Yf(e);
    },
    Qf = rn,
    eh = function () {
      var e = Qf(this),
        t = "";
      return e.hasIndices && (t += "d"), e.global && (t += "g"), e.ignoreCase && (t += "i"), e.multiline && (t += "m"), e.dotAll && (t += "s"), e.unicode && (t += "u"), e.unicodeSets && (t += "v"), e.sticky && (t += "y"), t;
    },
    th = _,
    nh = ft,
    rh = ye,
    ih = eh,
    oh = RegExp.prototype,
    ah = function (e) {
      var t = e.flags;
      return void 0 !== t || "flags" in oh || nh(e, "flags") || !rh(oh, e) ? t : th(ih, e);
    },
    sh = Cn.PROPER,
    uh = Pr,
    ch = rn,
    lh = Kf,
    fh = A,
    hh = ah,
    dh = "toString",
    ph = RegExp.prototype,
    gh = ph[dh],
    vh = fh(function () {
      return "/a/b" !== gh.call({
        source: "a",
        flags: "b"
      });
    }),
    yh = sh && gh.name !== dh;
  (vh || yh) && uh(ph, dh, function () {
    var e = ch(this);
    return "/" + lh(e.source) + "/" + lh(hh(e));
  }, {
    unsafe: !0
  });
  var mh = de,
    bh = Y,
    wh = Ct("match"),
    kh = function (e) {
      var t;
      return mh(e) && (void 0 !== (t = e[wh]) ? !!t : "RegExp" === bh(e));
    },
    Ph = kh,
    xh = TypeError,
    Sh = Ct("match"),
    Ch = Si,
    Eh = function (e) {
      if (Ph(e)) throw new xh("The method doesn't accept regular expressions");
      return e;
    },
    Th = ae,
    Oh = Kf,
    Ih = function (e) {
      var t = /./;
      try {
        "/./"[e](t);
      } catch (n) {
        try {
          return t[Sh] = !1, "/./"[e](t);
        } catch (r) {}
      }
      return !1;
    },
    Ah = W("".indexOf);
  Ch({
    target: "String",
    proto: !0,
    forced: !Ih("includes")
  }, {
    includes: function (e) {
      return !!~Ah(Oh(Th(this)), Oh(Eh(e)), arguments.length > 1 ? arguments[1] : void 0);
    }
  });
  var Lh = W,
    jh = Tr,
    Rh = Kf,
    Bh = ae,
    _h = Lh("".charAt),
    Nh = Lh("".charCodeAt),
    Fh = Lh("".slice),
    Mh = function (e) {
      return function (t, n) {
        var r,
          i,
          o = Rh(Bh(t)),
          a = jh(n),
          s = o.length;
        return a < 0 || a >= s ? e ? "" : void 0 : (r = Nh(o, a)) < 55296 || r > 56319 || a + 1 === s || (i = Nh(o, a + 1)) < 56320 || i > 57343 ? e ? _h(o, a) : r : e ? Fh(o, a, a + 2) : i - 56320 + (r - 55296 << 10) + 65536;
      };
    },
    Uh = {
      codeAt: Mh(!1),
      charAt: Mh(!0)
    },
    Dh = Uh.charAt,
    zh = Kf,
    Vh = Qn,
    qh = _f,
    $h = Nf,
    Gh = "String Iterator",
    Hh = Vh.set,
    Wh = Vh.getterFor(Gh);
  qh(String, "String", function (e) {
    Hh(this, {
      type: Gh,
      string: zh(e),
      index: 0
    });
  }, function () {
    var e,
      t = Wh(this),
      n = t.string,
      r = t.index;
    return r >= n.length ? $h(void 0, !0) : (e = Dh(n, r), t.index += e.length, $h(e, !1));
  });
  var Jh = !A(function () {
      return Object.isExtensible(Object.preventExtensions({}));
    }),
    Zh = Pr,
    Xh = function (e, t, n) {
      for (var r in t) Zh(e, r, t[r], n);
      return e;
    },
    Yh = {
      exports: {}
    },
    Kh = {},
    Qh = Y,
    ed = ce,
    td = xr.f,
    nd = Ca,
    rd = "object" == typeof window && window && Object.getOwnPropertyNames ? Object.getOwnPropertyNames(window) : [];
  Kh.f = function (e) {
    return rd && "Window" === Qh(e) ? function (e) {
      try {
        return td(e);
      } catch (UO) {
        return nd(rd);
      }
    }(e) : td(ed(e));
  };
  var id = A(function () {
      if ("function" == typeof ArrayBuffer) {
        var e = new ArrayBuffer(8);
        Object.isExtensible(e) && Object.defineProperty(e, "a", {
          value: 8
        });
      }
    }),
    od = A,
    ad = de,
    sd = Y,
    ud = id,
    cd = Object.isExtensible,
    ld = od(function () {
      cd(1);
    }) || ud ? function (e) {
      return !!ad(e) && (!ud || "ArrayBuffer" !== sd(e)) && (!cd || cd(e));
    } : cd,
    fd = Si,
    hd = W,
    dd = Un,
    pd = de,
    gd = ft,
    vd = Kt.f,
    yd = xr,
    md = Kh,
    bd = ld,
    wd = Jh,
    kd = !1,
    Pd = vt("meta"),
    xd = 0,
    Sd = function (e) {
      vd(e, Pd, {
        value: {
          objectID: "O" + xd++,
          weakData: {}
        }
      });
    },
    Cd = Yh.exports = {
      enable: function () {
        Cd.enable = function () {}, kd = !0;
        var e = yd.f,
          t = hd([].splice),
          n = {};
        n[Pd] = 1, e(n).length && (yd.f = function (n) {
          for (var r = e(n), i = 0, o = r.length; i < o; i++) if (r[i] === Pd) {
            t(r, i, 1);
            break;
          }
          return r;
        }, fd({
          target: "Object",
          stat: !0,
          forced: !0
        }, {
          getOwnPropertyNames: md.f
        }));
      },
      fastKey: function (e, t) {
        if (!pd(e)) return "symbol" == typeof e ? e : ("string" == typeof e ? "S" : "P") + e;
        if (!gd(e, Pd)) {
          if (!bd(e)) return "F";
          if (!t) return "E";
          Sd(e);
        }
        return e[Pd].objectID;
      },
      getWeakData: function (e, t) {
        if (!gd(e, Pd)) {
          if (!bd(e)) return !0;
          if (!t) return !1;
          Sd(e);
        }
        return e[Pd].weakData;
      },
      onFreeze: function (e) {
        return wd && kd && bd(e) && !gd(e, Pd) && Sd(e), e;
      }
    };
  dd[Pd] = !0;
  var Ed = Yh.exports,
    Td = fe,
    Od = de,
    Id = qo,
    Ad = function (e, t, n) {
      var r, i;
      return Id && Td(r = t.constructor) && r !== n && Od(i = r.prototype) && i !== n.prototype && Id(e, i), e;
    },
    Ld = Si,
    jd = O,
    Rd = W,
    Bd = vi,
    _d = Pr,
    Nd = Ed,
    Fd = Ac,
    Md = ia,
    Ud = fe,
    Dd = re,
    zd = de,
    Vd = A,
    qd = _c,
    $d = Wo,
    Gd = Ad,
    Hd = xa,
    Wd = ne,
    Jd = ut,
    Zd = Nr,
    Xd = ao,
    Yd = W([].push),
    Kd = function (e) {
      var t = 1 === e,
        n = 2 === e,
        r = 3 === e,
        i = 4 === e,
        o = 6 === e,
        a = 7 === e,
        s = 5 === e || o;
      return function (u, c, l, f) {
        for (var h, d, p = Jd(u), g = Wd(p), v = Zd(g), y = Hd(c, l), m = 0, b = f || Xd, w = t ? b(u, v) : n || a ? b(u, 0) : void 0; v > m; m++) if ((s || m in g) && (d = y(h = g[m], m, p), e)) if (t) w[m] = d;else if (d) switch (e) {
          case 3:
            return !0;
          case 5:
            return h;
          case 6:
            return m;
          case 2:
            Yd(w, h);
        } else switch (e) {
          case 4:
            return !1;
          case 7:
            Yd(w, h);
        }
        return o ? -1 : r || i ? i : w;
      };
    },
    Qd = {
      forEach: Kd(0),
      map: Kd(1),
      filter: Kd(2),
      some: Kd(3),
      every: Kd(4),
      find: Kd(5),
      findIndex: Kd(6),
      filterReject: Kd(7)
    },
    ep = W,
    tp = Xh,
    np = Ed.getWeakData,
    rp = ia,
    ip = rn,
    op = re,
    ap = de,
    sp = Ac,
    up = ft,
    cp = Qn.set,
    lp = Qn.getterFor,
    fp = Qd.find,
    hp = Qd.findIndex,
    dp = ep([].splice),
    pp = 0,
    gp = function (e) {
      return e.frozen || (e.frozen = new vp());
    },
    vp = function () {
      this.entries = [];
    },
    yp = function (e, t) {
      return fp(e.entries, function (e) {
        return e[0] === t;
      });
    };
  vp.prototype = {
    get: function (e) {
      var t = yp(this, e);
      if (t) return t[1];
    },
    has: function (e) {
      return !!yp(this, e);
    },
    set: function (e, t) {
      var n = yp(this, e);
      n ? n[1] = t : this.entries.push([e, t]);
    },
    delete: function (e) {
      var t = hp(this.entries, function (t) {
        return t[0] === e;
      });
      return ~t && dp(this.entries, t, 1), !!~t;
    }
  };
  var mp,
    bp = Jh,
    wp = O,
    kp = W,
    Pp = Xh,
    xp = Ed,
    Sp = function (e, t, n) {
      var r = -1 !== e.indexOf("Map"),
        i = -1 !== e.indexOf("Weak"),
        o = r ? "set" : "add",
        a = jd[e],
        s = a && a.prototype,
        u = a,
        c = {},
        l = function (e) {
          var t = Rd(s[e]);
          _d(s, e, "add" === e ? function (e) {
            return t(this, 0 === e ? 0 : e), this;
          } : "delete" === e ? function (e) {
            return !(i && !zd(e)) && t(this, 0 === e ? 0 : e);
          } : "get" === e ? function (e) {
            return i && !zd(e) ? void 0 : t(this, 0 === e ? 0 : e);
          } : "has" === e ? function (e) {
            return !(i && !zd(e)) && t(this, 0 === e ? 0 : e);
          } : function (e, n) {
            return t(this, 0 === e ? 0 : e, n), this;
          });
        };
      if (Bd(e, !Ud(a) || !(i || s.forEach && !Vd(function () {
        new a().entries().next();
      })))) u = n.getConstructor(t, e, r, o), Nd.enable();else if (Bd(e, !0)) {
        var f = new u(),
          h = f[o](i ? {} : -0, 1) !== f,
          d = Vd(function () {
            f.has(1);
          }),
          p = qd(function (e) {
            new a(e);
          }),
          g = !i && Vd(function () {
            for (var e = new a(), t = 5; t--;) e[o](t, t);
            return !e.has(-0);
          });
        p || ((u = t(function (e, t) {
          Md(e, s);
          var n = Gd(new a(), e, u);
          return Dd(t) || Fd(t, n[o], {
            that: n,
            AS_ENTRIES: r
          }), n;
        })).prototype = s, s.constructor = u), (d || g) && (l("delete"), l("has"), r && l("get")), (g || h) && l(o), i && s.clear && delete s.clear;
      }
      return c[e] = u, Ld({
        global: !0,
        constructor: !0,
        forced: u !== a
      }, c), $d(u, e), i || n.setStrong(u, e, r), u;
    },
    Cp = {
      getConstructor: function (e, t, n, r) {
        var i = e(function (e, i) {
            rp(e, o), cp(e, {
              type: t,
              id: pp++,
              frozen: void 0
            }), op(i) || sp(i, e[r], {
              that: e,
              AS_ENTRIES: n
            });
          }),
          o = i.prototype,
          a = lp(t),
          s = function (e, t, n) {
            var r = a(e),
              i = np(ip(t), !0);
            return !0 === i ? gp(r).set(t, n) : i[r.id] = n, e;
          };
        return tp(o, {
          delete: function (e) {
            var t = a(this);
            if (!ap(e)) return !1;
            var n = np(e);
            return !0 === n ? gp(t).delete(e) : n && up(n, t.id) && delete n[t.id];
          },
          has: function (e) {
            var t = a(this);
            if (!ap(e)) return !1;
            var n = np(e);
            return !0 === n ? gp(t).has(e) : n && up(n, t.id);
          }
        }), tp(o, n ? {
          get: function (e) {
            var t = a(this);
            if (ap(e)) {
              var n = np(e);
              return !0 === n ? gp(t).get(e) : n ? n[t.id] : void 0;
            }
          },
          set: function (e, t) {
            return s(this, e, t);
          }
        } : {
          add: function (e) {
            return s(this, e, !0);
          }
        }), i;
      }
    },
    Ep = de,
    Tp = Qn.enforce,
    Op = A,
    Ip = _n,
    Ap = Object,
    Lp = Array.isArray,
    jp = Ap.isExtensible,
    Rp = Ap.isFrozen,
    Bp = Ap.isSealed,
    _p = Ap.freeze,
    Np = Ap.seal,
    Fp = !wp.ActiveXObject && "ActiveXObject" in wp,
    Mp = function (e) {
      return function () {
        return e(this, arguments.length ? arguments[0] : void 0);
      };
    },
    Up = Sp("WeakMap", Mp, Cp),
    Dp = Up.prototype,
    zp = kp(Dp.set);
  if (Ip) if (Fp) {
    mp = Cp.getConstructor(Mp, "WeakMap", !0), xp.enable();
    var Vp = kp(Dp.delete),
      qp = kp(Dp.has),
      $p = kp(Dp.get);
    Pp(Dp, {
      delete: function (e) {
        if (Ep(e) && !jp(e)) {
          var t = Tp(this);
          return t.frozen || (t.frozen = new mp()), Vp(this, e) || t.frozen.delete(e);
        }
        return Vp(this, e);
      },
      has: function (e) {
        if (Ep(e) && !jp(e)) {
          var t = Tp(this);
          return t.frozen || (t.frozen = new mp()), qp(this, e) || t.frozen.has(e);
        }
        return qp(this, e);
      },
      get: function (e) {
        if (Ep(e) && !jp(e)) {
          var t = Tp(this);
          return t.frozen || (t.frozen = new mp()), qp(this, e) ? $p(this, e) : t.frozen.get(e);
        }
        return $p(this, e);
      },
      set: function (e, t) {
        if (Ep(e) && !jp(e)) {
          var n = Tp(this);
          n.frozen || (n.frozen = new mp()), qp(this, e) ? zp(this, e, t) : n.frozen.set(e, t);
        } else zp(this, e, t);
        return this;
      }
    });
  } else (function () {
    return bp && Op(function () {
      var e = _p([]);
      return zp(new Up(), e, 1), !Rp(e);
    });
  })() && Pp(Dp, {
    set: function (e, t) {
      var n;
      return Lp(e) && (Rp(e) ? n = _p : Bp(e) && (n = Np)), zp(this, e, t), n && n(e), this;
    }
  });
  var Gp = {
      CSSRuleList: 0,
      CSSStyleDeclaration: 0,
      CSSValueList: 0,
      ClientRectList: 0,
      DOMRectList: 0,
      DOMStringList: 0,
      DOMTokenList: 1,
      DataTransferItemList: 0,
      FileList: 0,
      HTMLAllCollection: 0,
      HTMLCollection: 0,
      HTMLFormElement: 0,
      HTMLSelectElement: 0,
      MediaList: 0,
      MimeTypeArray: 0,
      NamedNodeMap: 0,
      NodeList: 1,
      PaintRequestList: 0,
      Plugin: 0,
      PluginArray: 0,
      SVGLengthList: 0,
      SVGNumberList: 0,
      SVGPathSegList: 0,
      SVGPointList: 0,
      SVGStringList: 0,
      SVGTransformList: 0,
      SourceBufferList: 0,
      StyleSheetList: 0,
      TextTrackCueList: 0,
      TextTrackList: 0,
      TouchList: 0
    },
    Hp = Dt("span").classList,
    Wp = Hp && Hp.constructor && Hp.constructor.prototype,
    Jp = Wp === Object.prototype ? void 0 : Wp,
    Zp = O,
    Xp = Gp,
    Yp = Jp,
    Kp = Jf,
    Qp = mn,
    eg = Wo,
    tg = Ct("iterator"),
    ng = Kp.values,
    rg = function (e, t) {
      if (e) {
        if (e[tg] !== ng) try {
          Qp(e, tg, ng);
        } catch (UO) {
          e[tg] = ng;
        }
        if (eg(e, t, !0), Xp[t]) for (var n in Kp) if (e[n] !== Kp[n]) try {
          Qp(e, n, Kp[n]);
        } catch (UO) {
          e[n] = Kp[n];
        }
      }
    };
  for (var ig in Xp) rg(Zp[ig] && Zp[ig].prototype, ig);
  rg(Yp, "DOMTokenList");
  var og = A,
    ag = L,
    sg = Ct("iterator"),
    ug = !og(function () {
      var e = new URL("b?a=1&b=2&c=3", "http://a"),
        t = e.searchParams,
        n = new URLSearchParams("a=1&a=2&b=3"),
        r = "";
      return e.pathname = "c%20d", t.forEach(function (e, n) {
        t.delete("b"), r += n + e;
      }), n.delete("a", 2), n.delete("b", void 0), !t.size && !ag || !t.sort || "http://a/c%20d?a=1&c=3" !== e.href || "3" !== t.get("c") || "a=1" !== String(new URLSearchParams("?a=1")) || !t[sg] || "a" !== new URL("https://a@b").username || "b" !== new URLSearchParams(new URLSearchParams("a=b")).get("a") || "xn--e1aybc" !== new URL("http://тест").host || "#%D0%B1" !== new URL("http://a#б").hash || "a1c3" !== r || "x" !== new URL("http://x", void 0).host;
    }),
    cg = L,
    lg = W,
    fg = _,
    hg = A,
    dg = hl,
    pg = Yr,
    gg = N,
    vg = ut,
    yg = ne,
    mg = Object.assign,
    bg = Object.defineProperty,
    wg = lg([].concat),
    kg = !mg || hg(function () {
      if (cg && 1 !== mg({
        b: 1
      }, mg(bg({}, "a", {
        enumerable: !0,
        get: function () {
          bg(this, "b", {
            value: 3,
            enumerable: !1
          });
        }
      }), {
        b: 2
      })).b) return !0;
      var e = {},
        t = {},
        n = Symbol("assign detection"),
        r = "abcdefghijklmnopqrst";
      return e[n] = 7, r.split("").forEach(function (e) {
        t[e] = e;
      }), 7 !== mg({}, e)[n] || dg(mg({}, t)).join("") !== r;
    }) ? function (e, t) {
      for (var n = vg(e), r = arguments.length, i = 1, o = pg.f, a = gg.f; r > i;) for (var s, u = yg(arguments[i++]), c = o ? wg(dg(u), o(u)) : dg(u), l = c.length, f = 0; l > f;) s = c[f++], cg && !fg(a, u, s) || (n[s] = u[s]);
      return n;
    } : mg,
    Pg = rn,
    xg = vc,
    Sg = xa,
    Cg = _,
    Eg = ut,
    Tg = function (e, t, n, r) {
      try {
        return r ? t(Pg(n)[0], n[1]) : t(n);
      } catch (UO) {
        xg(e, "throw", UO);
      }
    },
    Og = Qu,
    Ig = Qi,
    Ag = Nr,
    Lg = Li,
    jg = hc,
    Rg = oc,
    Bg = Array,
    _g = function (e) {
      var t = Eg(e),
        n = Ig(this),
        r = arguments.length,
        i = r > 1 ? arguments[1] : void 0,
        o = void 0 !== i;
      o && (i = Sg(i, r > 2 ? arguments[2] : void 0));
      var a,
        s,
        u,
        c,
        l,
        f,
        h = Rg(t),
        d = 0;
      if (!h || this === Bg && Og(h)) for (a = Ag(t), s = n ? new this(a) : Bg(a); a > d; d++) f = o ? i(t[d], d) : t[d], Lg(s, d, f);else for (s = n ? new this() : [], l = (c = jg(t, h)).next; !(u = Cg(l, c)).done; d++) f = o ? Tg(c, i, [u.value, d], !0) : u.value, Lg(s, d, f);
      return s.length = d, s;
    },
    Ng = W,
    Fg = 2147483647,
    Mg = /[^\0-\u007E]/,
    Ug = /[.\u3002\uFF0E\uFF61]/g,
    Dg = "Overflow: input needs wider integers to process",
    zg = RangeError,
    Vg = Ng(Ug.exec),
    qg = Math.floor,
    $g = String.fromCharCode,
    Gg = Ng("".charCodeAt),
    Hg = Ng([].join),
    Wg = Ng([].push),
    Jg = Ng("".replace),
    Zg = Ng("".split),
    Xg = Ng("".toLowerCase),
    Yg = function (e) {
      return e + 22 + 75 * (e < 26);
    },
    Kg = function (e, t, n) {
      var r = 0;
      for (e = n ? qg(e / 700) : e >> 1, e += qg(e / t); e > 455;) e = qg(e / 35), r += 36;
      return qg(r + 36 * e / (e + 38));
    },
    Qg = function (e) {
      var t = [];
      e = function (e) {
        for (var t = [], n = 0, r = e.length; n < r;) {
          var i = Gg(e, n++);
          if (i >= 55296 && i <= 56319 && n < r) {
            var o = Gg(e, n++);
            56320 == (64512 & o) ? Wg(t, ((1023 & i) << 10) + (1023 & o) + 65536) : (Wg(t, i), n--);
          } else Wg(t, i);
        }
        return t;
      }(e);
      var n,
        r,
        i = e.length,
        o = 128,
        a = 0,
        s = 72;
      for (n = 0; n < e.length; n++) (r = e[n]) < 128 && Wg(t, $g(r));
      var u = t.length,
        c = u;
      for (u && Wg(t, "-"); c < i;) {
        var l = Fg;
        for (n = 0; n < e.length; n++) (r = e[n]) >= o && r < l && (l = r);
        var f = c + 1;
        if (l - o > qg((Fg - a) / f)) throw new zg(Dg);
        for (a += (l - o) * f, o = l, n = 0; n < e.length; n++) {
          if ((r = e[n]) < o && ++a > Fg) throw new zg(Dg);
          if (r === o) {
            for (var h = a, d = 36;;) {
              var p = d <= s ? 1 : d >= s + 26 ? 26 : d - s;
              if (h < p) break;
              var g = h - p,
                v = 36 - p;
              Wg(t, $g(Yg(p + g % v))), h = qg(g / v), d += 36;
            }
            Wg(t, $g(Yg(h))), s = Kg(a, f, c === u), a = 0, c++;
          }
        }
        a++, o++;
      }
      return Hg(t, "");
    },
    ev = Ca,
    tv = Math.floor,
    nv = function (e, t) {
      var n = e.length;
      if (n < 8) for (var r, i, o = 1; o < n;) {
        for (i = o, r = e[o]; i && t(e[i - 1], r) > 0;) e[i] = e[--i];
        i !== o++ && (e[i] = r);
      } else for (var a = tv(n / 2), s = nv(ev(e, 0, a), t), u = nv(ev(e, a), t), c = s.length, l = u.length, f = 0, h = 0; f < c || h < l;) e[f + h] = f < c && h < l ? t(s[f], u[h]) <= 0 ? s[f++] : u[h++] : f < c ? s[f++] : u[h++];
      return e;
    },
    rv = Si,
    iv = O,
    ov = os,
    av = _,
    sv = W,
    uv = L,
    cv = ug,
    lv = Pr,
    fv = Xo,
    hv = Xh,
    dv = Wo,
    pv = gf,
    gv = Qn,
    vv = ia,
    yv = fe,
    mv = ft,
    bv = xa,
    wv = Di,
    kv = rn,
    Pv = de,
    xv = Kf,
    Sv = Rl,
    Cv = V,
    Ev = hc,
    Tv = oc,
    Ov = Nf,
    Iv = Ta,
    Av = nv,
    Lv = Ct("iterator"),
    jv = "URLSearchParams",
    Rv = jv + "Iterator",
    Bv = gv.set,
    _v = gv.getterFor(jv),
    Nv = gv.getterFor(Rv),
    Fv = ov("fetch"),
    Mv = ov("Request"),
    Uv = ov("Headers"),
    Dv = Mv && Mv.prototype,
    zv = Uv && Uv.prototype,
    Vv = iv.RegExp,
    qv = iv.TypeError,
    $v = iv.decodeURIComponent,
    Gv = iv.encodeURIComponent,
    Hv = sv("".charAt),
    Wv = sv([].join),
    Jv = sv([].push),
    Zv = sv("".replace),
    Xv = sv([].shift),
    Yv = sv([].splice),
    Kv = sv("".split),
    Qv = sv("".slice),
    ey = /\+/g,
    ty = Array(4),
    ny = function (e) {
      return ty[e - 1] || (ty[e - 1] = Vv("((?:%[\\da-f]{2}){" + e + "})", "gi"));
    },
    ry = function (e) {
      try {
        return $v(e);
      } catch (UO) {
        return e;
      }
    },
    iy = function (e) {
      var t = Zv(e, ey, " "),
        n = 4;
      try {
        return $v(t);
      } catch (UO) {
        for (; n;) t = Zv(t, ny(n--), ry);
        return t;
      }
    },
    oy = /[!'()~]|%20/g,
    ay = {
      "!": "%21",
      "'": "%27",
      "(": "%28",
      ")": "%29",
      "~": "%7E",
      "%20": "+"
    },
    sy = function (e) {
      return ay[e];
    },
    uy = function (e) {
      return Zv(Gv(e), oy, sy);
    },
    cy = pv(function (e, t) {
      Bv(this, {
        type: Rv,
        target: _v(e).entries,
        index: 0,
        kind: t
      });
    }, jv, function () {
      var e = Nv(this),
        t = e.target,
        n = e.index++;
      if (!t || n >= t.length) return e.target = void 0, Ov(void 0, !0);
      var r = t[n];
      switch (e.kind) {
        case "keys":
          return Ov(r.key, !1);
        case "values":
          return Ov(r.value, !1);
      }
      return Ov([r.key, r.value], !1);
    }, !0),
    ly = function (e) {
      this.entries = [], this.url = null, void 0 !== e && (Pv(e) ? this.parseObject(e) : this.parseQuery("string" == typeof e ? "?" === Hv(e, 0) ? Qv(e, 1) : e : xv(e)));
    };
  ly.prototype = {
    type: jv,
    bindURL: function (e) {
      this.url = e, this.update();
    },
    parseObject: function (e) {
      var t,
        n,
        r,
        i,
        o,
        a,
        s,
        u = this.entries,
        c = Tv(e);
      if (c) for (n = (t = Ev(e, c)).next; !(r = av(n, t)).done;) {
        if (o = (i = Ev(kv(r.value))).next, (a = av(o, i)).done || (s = av(o, i)).done || !av(o, i).done) throw new qv("Expected sequence with length 2");
        Jv(u, {
          key: xv(a.value),
          value: xv(s.value)
        });
      } else for (var l in e) mv(e, l) && Jv(u, {
        key: l,
        value: xv(e[l])
      });
    },
    parseQuery: function (e) {
      if (e) for (var t, n, r = this.entries, i = Kv(e, "&"), o = 0; o < i.length;) (t = i[o++]).length && (n = Kv(t, "="), Jv(r, {
        key: iy(Xv(n)),
        value: iy(Wv(n, "="))
      }));
    },
    serialize: function () {
      for (var e, t = this.entries, n = [], r = 0; r < t.length;) e = t[r++], Jv(n, uy(e.key) + "=" + uy(e.value));
      return Wv(n, "&");
    },
    update: function () {
      this.entries.length = 0, this.parseQuery(this.url.query);
    },
    updateURL: function () {
      this.url && this.url.update();
    }
  };
  var fy = function () {
      vv(this, hy);
      var e = Bv(this, new ly(arguments.length > 0 ? arguments[0] : void 0));
      uv || (this.size = e.entries.length);
    },
    hy = fy.prototype;
  if (hv(hy, {
    append: function (e, t) {
      var n = _v(this);
      Iv(arguments.length, 2), Jv(n.entries, {
        key: xv(e),
        value: xv(t)
      }), uv || this.length++, n.updateURL();
    },
    delete: function (e) {
      for (var t = _v(this), n = Iv(arguments.length, 1), r = t.entries, i = xv(e), o = n < 2 ? void 0 : arguments[1], a = void 0 === o ? o : xv(o), s = 0; s < r.length;) {
        var u = r[s];
        if (u.key !== i || void 0 !== a && u.value !== a) s++;else if (Yv(r, s, 1), void 0 !== a) break;
      }
      uv || (this.size = r.length), t.updateURL();
    },
    get: function (e) {
      var t = _v(this).entries;
      Iv(arguments.length, 1);
      for (var n = xv(e), r = 0; r < t.length; r++) if (t[r].key === n) return t[r].value;
      return null;
    },
    getAll: function (e) {
      var t = _v(this).entries;
      Iv(arguments.length, 1);
      for (var n = xv(e), r = [], i = 0; i < t.length; i++) t[i].key === n && Jv(r, t[i].value);
      return r;
    },
    has: function (e) {
      for (var t = _v(this).entries, n = Iv(arguments.length, 1), r = xv(e), i = n < 2 ? void 0 : arguments[1], o = void 0 === i ? i : xv(i), a = 0; a < t.length;) {
        var s = t[a++];
        if (s.key === r && (void 0 === o || s.value === o)) return !0;
      }
      return !1;
    },
    set: function (e, t) {
      var n = _v(this);
      Iv(arguments.length, 1);
      for (var r, i = n.entries, o = !1, a = xv(e), s = xv(t), u = 0; u < i.length; u++) (r = i[u]).key === a && (o ? Yv(i, u--, 1) : (o = !0, r.value = s));
      o || Jv(i, {
        key: a,
        value: s
      }), uv || (this.size = i.length), n.updateURL();
    },
    sort: function () {
      var e = _v(this);
      Av(e.entries, function (e, t) {
        return e.key > t.key ? 1 : -1;
      }), e.updateURL();
    },
    forEach: function (e) {
      for (var t, n = _v(this).entries, r = bv(e, arguments.length > 1 ? arguments[1] : void 0), i = 0; i < n.length;) r((t = n[i++]).value, t.key, this);
    },
    keys: function () {
      return new cy(this, "keys");
    },
    values: function () {
      return new cy(this, "values");
    },
    entries: function () {
      return new cy(this, "entries");
    }
  }, {
    enumerable: !0
  }), lv(hy, Lv, hy.entries, {
    name: "entries"
  }), lv(hy, "toString", function () {
    return _v(this).serialize();
  }, {
    enumerable: !0
  }), uv && fv(hy, "size", {
    get: function () {
      return _v(this).entries.length;
    },
    configurable: !0,
    enumerable: !0
  }), dv(fy, jv), rv({
    global: !0,
    constructor: !0,
    forced: !cv
  }, {
    URLSearchParams: fy
  }), !cv && yv(Uv)) {
    var dy = sv(zv.has),
      py = sv(zv.set),
      gy = function (e) {
        if (Pv(e)) {
          var t,
            n = e.body;
          if (wv(n) === jv) return t = e.headers ? new Uv(e.headers) : new Uv(), dy(t, "content-type") || py(t, "content-type", "application/x-www-form-urlencoded;charset=UTF-8"), Sv(e, {
            body: Cv(0, xv(n)),
            headers: Cv(0, t)
          });
        }
        return e;
      };
    if (yv(Fv) && rv({
      global: !0,
      enumerable: !0,
      dontCallGetSet: !0,
      forced: !0
    }, {
      fetch: function (e) {
        return Fv(e, arguments.length > 1 ? gy(arguments[1]) : {});
      }
    }), yv(Mv)) {
      var vy = function (e) {
        return vv(this, Dv), new Mv(e, arguments.length > 1 ? gy(arguments[1]) : {});
      };
      Dv.constructor = vy, vy.prototype = Dv, rv({
        global: !0,
        constructor: !0,
        dontCallGetSet: !0,
        forced: !0
      }, {
        Request: vy
      });
    }
  }
  var yy,
    my = Si,
    by = L,
    wy = ug,
    ky = O,
    Py = xa,
    xy = W,
    Sy = Pr,
    Cy = Xo,
    Ey = ia,
    Ty = ft,
    Oy = kg,
    Iy = _g,
    Ay = Ca,
    Ly = Uh.codeAt,
    jy = function (e) {
      var t,
        n,
        r = [],
        i = Zg(Jg(Xg(e), Ug, "."), ".");
      for (t = 0; t < i.length; t++) n = i[t], Wg(r, Vg(Mg, n) ? "xn--" + Qg(n) : n);
      return Hg(r, ".");
    },
    Ry = Kf,
    By = Wo,
    _y = Ta,
    Ny = {
      URLSearchParams: fy,
      getState: _v
    },
    Fy = Qn,
    My = Fy.set,
    Uy = Fy.getterFor("URL"),
    Dy = Ny.URLSearchParams,
    zy = Ny.getState,
    Vy = ky.URL,
    qy = ky.TypeError,
    $y = ky.parseInt,
    Gy = Math.floor,
    Hy = Math.pow,
    Wy = xy("".charAt),
    Jy = xy(/./.exec),
    Zy = xy([].join),
    Xy = xy(1..toString),
    Yy = xy([].pop),
    Ky = xy([].push),
    Qy = xy("".replace),
    em = xy([].shift),
    tm = xy("".split),
    nm = xy("".slice),
    rm = xy("".toLowerCase),
    im = xy([].unshift),
    om = "Invalid scheme",
    am = "Invalid host",
    sm = "Invalid port",
    um = /[a-z]/i,
    cm = /[\d+-.a-z]/i,
    lm = /\d/,
    fm = /^0x/i,
    hm = /^[0-7]+$/,
    dm = /^\d+$/,
    pm = /^[\da-f]+$/i,
    gm = /[\0\t\n\r #%/:<>?@[\\\]^|]/,
    vm = /[\0\t\n\r #/:<>?@[\\\]^|]/,
    ym = /^[\u0000-\u0020]+/,
    mm = /(^|[^\u0000-\u0020])[\u0000-\u0020]+$/,
    bm = /[\t\n\r]/g,
    wm = function (e) {
      var t, n, r, i;
      if ("number" == typeof e) {
        for (t = [], n = 0; n < 4; n++) im(t, e % 256), e = Gy(e / 256);
        return Zy(t, ".");
      }
      if ("object" == typeof e) {
        for (t = "", r = function (e) {
          for (var t = null, n = 1, r = null, i = 0, o = 0; o < 8; o++) 0 !== e[o] ? (i > n && (t = r, n = i), r = null, i = 0) : (null === r && (r = o), ++i);
          return i > n && (t = r, n = i), t;
        }(e), n = 0; n < 8; n++) i && 0 === e[n] || (i && (i = !1), r === n ? (t += n ? ":" : "::", i = !0) : (t += Xy(e[n], 16), n < 7 && (t += ":")));
        return "[" + t + "]";
      }
      return e;
    },
    km = {},
    Pm = Oy({}, km, {
      " ": 1,
      '"': 1,
      "<": 1,
      ">": 1,
      "`": 1
    }),
    xm = Oy({}, Pm, {
      "#": 1,
      "?": 1,
      "{": 1,
      "}": 1
    }),
    Sm = Oy({}, xm, {
      "/": 1,
      ":": 1,
      ";": 1,
      "=": 1,
      "@": 1,
      "[": 1,
      "\\": 1,
      "]": 1,
      "^": 1,
      "|": 1
    }),
    Cm = function (e, t) {
      var n = Ly(e, 0);
      return n > 32 && n < 127 && !Ty(t, e) ? e : encodeURIComponent(e);
    },
    Em = {
      ftp: 21,
      file: null,
      http: 80,
      https: 443,
      ws: 80,
      wss: 443
    },
    Tm = function (e, t) {
      var n;
      return 2 === e.length && Jy(um, Wy(e, 0)) && (":" === (n = Wy(e, 1)) || !t && "|" === n);
    },
    Om = function (e) {
      var t;
      return e.length > 1 && Tm(nm(e, 0, 2)) && (2 === e.length || "/" === (t = Wy(e, 2)) || "\\" === t || "?" === t || "#" === t);
    },
    Im = function (e) {
      return "." === e || "%2e" === rm(e);
    },
    Am = function (e) {
      return ".." === (e = rm(e)) || "%2e." === e || ".%2e" === e || "%2e%2e" === e;
    },
    Lm = {},
    jm = {},
    Rm = {},
    Bm = {},
    _m = {},
    Nm = {},
    Fm = {},
    Mm = {},
    Um = {},
    Dm = {},
    zm = {},
    Vm = {},
    qm = {},
    $m = {},
    Gm = {},
    Hm = {},
    Wm = {},
    Jm = {},
    Zm = {},
    Xm = {},
    Ym = {},
    Km = function (e, t, n) {
      var r,
        i,
        o,
        a = Ry(e);
      if (t) {
        if (i = this.parse(a)) throw new qy(i);
        this.searchParams = null;
      } else {
        if (void 0 !== n && (r = new Km(n, !0)), i = this.parse(a, null, r)) throw new qy(i);
        (o = zy(new Dy())).bindURL(this), this.searchParams = o;
      }
    };
  Km.prototype = {
    type: "URL",
    parse: function (e, t, n) {
      var r,
        i,
        o,
        a,
        s = this,
        u = t || Lm,
        c = 0,
        l = "",
        f = !1,
        h = !1,
        d = !1;
      for (e = Ry(e), t || (s.scheme = "", s.username = "", s.password = "", s.host = null, s.port = null, s.path = [], s.query = null, s.fragment = null, s.cannotBeABaseURL = !1, e = Qy(e, ym, ""), e = Qy(e, mm, "$1")), e = Qy(e, bm, ""), r = Iy(e); c <= r.length;) {
        switch (i = r[c], u) {
          case Lm:
            if (!i || !Jy(um, i)) {
              if (t) return om;
              u = Rm;
              continue;
            }
            l += rm(i), u = jm;
            break;
          case jm:
            if (i && (Jy(cm, i) || "+" === i || "-" === i || "." === i)) l += rm(i);else {
              if (":" !== i) {
                if (t) return om;
                l = "", u = Rm, c = 0;
                continue;
              }
              if (t && (s.isSpecial() !== Ty(Em, l) || "file" === l && (s.includesCredentials() || null !== s.port) || "file" === s.scheme && !s.host)) return;
              if (s.scheme = l, t) return void (s.isSpecial() && Em[s.scheme] === s.port && (s.port = null));
              l = "", "file" === s.scheme ? u = $m : s.isSpecial() && n && n.scheme === s.scheme ? u = Bm : s.isSpecial() ? u = Mm : "/" === r[c + 1] ? (u = _m, c++) : (s.cannotBeABaseURL = !0, Ky(s.path, ""), u = Zm);
            }
            break;
          case Rm:
            if (!n || n.cannotBeABaseURL && "#" !== i) return om;
            if (n.cannotBeABaseURL && "#" === i) {
              s.scheme = n.scheme, s.path = Ay(n.path), s.query = n.query, s.fragment = "", s.cannotBeABaseURL = !0, u = Ym;
              break;
            }
            u = "file" === n.scheme ? $m : Nm;
            continue;
          case Bm:
            if ("/" !== i || "/" !== r[c + 1]) {
              u = Nm;
              continue;
            }
            u = Um, c++;
            break;
          case _m:
            if ("/" === i) {
              u = Dm;
              break;
            }
            u = Jm;
            continue;
          case Nm:
            if (s.scheme = n.scheme, i === yy) s.username = n.username, s.password = n.password, s.host = n.host, s.port = n.port, s.path = Ay(n.path), s.query = n.query;else if ("/" === i || "\\" === i && s.isSpecial()) u = Fm;else if ("?" === i) s.username = n.username, s.password = n.password, s.host = n.host, s.port = n.port, s.path = Ay(n.path), s.query = "", u = Xm;else {
              if ("#" !== i) {
                s.username = n.username, s.password = n.password, s.host = n.host, s.port = n.port, s.path = Ay(n.path), s.path.length--, u = Jm;
                continue;
              }
              s.username = n.username, s.password = n.password, s.host = n.host, s.port = n.port, s.path = Ay(n.path), s.query = n.query, s.fragment = "", u = Ym;
            }
            break;
          case Fm:
            if (!s.isSpecial() || "/" !== i && "\\" !== i) {
              if ("/" !== i) {
                s.username = n.username, s.password = n.password, s.host = n.host, s.port = n.port, u = Jm;
                continue;
              }
              u = Dm;
            } else u = Um;
            break;
          case Mm:
            if (u = Um, "/" !== i || "/" !== Wy(l, c + 1)) continue;
            c++;
            break;
          case Um:
            if ("/" !== i && "\\" !== i) {
              u = Dm;
              continue;
            }
            break;
          case Dm:
            if ("@" === i) {
              f && (l = "%40" + l), f = !0, o = Iy(l);
              for (var p = 0; p < o.length; p++) {
                var g = o[p];
                if (":" !== g || d) {
                  var v = Cm(g, Sm);
                  d ? s.password += v : s.username += v;
                } else d = !0;
              }
              l = "";
            } else if (i === yy || "/" === i || "?" === i || "#" === i || "\\" === i && s.isSpecial()) {
              if (f && "" === l) return "Invalid authority";
              c -= Iy(l).length + 1, l = "", u = zm;
            } else l += i;
            break;
          case zm:
          case Vm:
            if (t && "file" === s.scheme) {
              u = Hm;
              continue;
            }
            if (":" !== i || h) {
              if (i === yy || "/" === i || "?" === i || "#" === i || "\\" === i && s.isSpecial()) {
                if (s.isSpecial() && "" === l) return am;
                if (t && "" === l && (s.includesCredentials() || null !== s.port)) return;
                if (a = s.parseHost(l)) return a;
                if (l = "", u = Wm, t) return;
                continue;
              }
              "[" === i ? h = !0 : "]" === i && (h = !1), l += i;
            } else {
              if ("" === l) return am;
              if (a = s.parseHost(l)) return a;
              if (l = "", u = qm, t === Vm) return;
            }
            break;
          case qm:
            if (!Jy(lm, i)) {
              if (i === yy || "/" === i || "?" === i || "#" === i || "\\" === i && s.isSpecial() || t) {
                if ("" !== l) {
                  var y = $y(l, 10);
                  if (y > 65535) return sm;
                  s.port = s.isSpecial() && y === Em[s.scheme] ? null : y, l = "";
                }
                if (t) return;
                u = Wm;
                continue;
              }
              return sm;
            }
            l += i;
            break;
          case $m:
            if (s.scheme = "file", "/" === i || "\\" === i) u = Gm;else {
              if (!n || "file" !== n.scheme) {
                u = Jm;
                continue;
              }
              switch (i) {
                case yy:
                  s.host = n.host, s.path = Ay(n.path), s.query = n.query;
                  break;
                case "?":
                  s.host = n.host, s.path = Ay(n.path), s.query = "", u = Xm;
                  break;
                case "#":
                  s.host = n.host, s.path = Ay(n.path), s.query = n.query, s.fragment = "", u = Ym;
                  break;
                default:
                  Om(Zy(Ay(r, c), "")) || (s.host = n.host, s.path = Ay(n.path), s.shortenPath()), u = Jm;
                  continue;
              }
            }
            break;
          case Gm:
            if ("/" === i || "\\" === i) {
              u = Hm;
              break;
            }
            n && "file" === n.scheme && !Om(Zy(Ay(r, c), "")) && (Tm(n.path[0], !0) ? Ky(s.path, n.path[0]) : s.host = n.host), u = Jm;
            continue;
          case Hm:
            if (i === yy || "/" === i || "\\" === i || "?" === i || "#" === i) {
              if (!t && Tm(l)) u = Jm;else if ("" === l) {
                if (s.host = "", t) return;
                u = Wm;
              } else {
                if (a = s.parseHost(l)) return a;
                if ("localhost" === s.host && (s.host = ""), t) return;
                l = "", u = Wm;
              }
              continue;
            }
            l += i;
            break;
          case Wm:
            if (s.isSpecial()) {
              if (u = Jm, "/" !== i && "\\" !== i) continue;
            } else if (t || "?" !== i) {
              if (t || "#" !== i) {
                if (i !== yy && (u = Jm, "/" !== i)) continue;
              } else s.fragment = "", u = Ym;
            } else s.query = "", u = Xm;
            break;
          case Jm:
            if (i === yy || "/" === i || "\\" === i && s.isSpecial() || !t && ("?" === i || "#" === i)) {
              if (Am(l) ? (s.shortenPath(), "/" === i || "\\" === i && s.isSpecial() || Ky(s.path, "")) : Im(l) ? "/" === i || "\\" === i && s.isSpecial() || Ky(s.path, "") : ("file" === s.scheme && !s.path.length && Tm(l) && (s.host && (s.host = ""), l = Wy(l, 0) + ":"), Ky(s.path, l)), l = "", "file" === s.scheme && (i === yy || "?" === i || "#" === i)) for (; s.path.length > 1 && "" === s.path[0];) em(s.path);
              "?" === i ? (s.query = "", u = Xm) : "#" === i && (s.fragment = "", u = Ym);
            } else l += Cm(i, xm);
            break;
          case Zm:
            "?" === i ? (s.query = "", u = Xm) : "#" === i ? (s.fragment = "", u = Ym) : i !== yy && (s.path[0] += Cm(i, km));
            break;
          case Xm:
            t || "#" !== i ? i !== yy && ("'" === i && s.isSpecial() ? s.query += "%27" : s.query += "#" === i ? "%23" : Cm(i, km)) : (s.fragment = "", u = Ym);
            break;
          case Ym:
            i !== yy && (s.fragment += Cm(i, Pm));
        }
        c++;
      }
    },
    parseHost: function (e) {
      var t, n, r;
      if ("[" === Wy(e, 0)) {
        if ("]" !== Wy(e, e.length - 1)) return am;
        if (t = function (e) {
          var t,
            n,
            r,
            i,
            o,
            a,
            s,
            u = [0, 0, 0, 0, 0, 0, 0, 0],
            c = 0,
            l = null,
            f = 0,
            h = function () {
              return Wy(e, f);
            };
          if (":" === h()) {
            if (":" !== Wy(e, 1)) return;
            f += 2, l = ++c;
          }
          for (; h();) {
            if (8 === c) return;
            if (":" !== h()) {
              for (t = n = 0; n < 4 && Jy(pm, h());) t = 16 * t + $y(h(), 16), f++, n++;
              if ("." === h()) {
                if (0 === n) return;
                if (f -= n, c > 6) return;
                for (r = 0; h();) {
                  if (i = null, r > 0) {
                    if (!("." === h() && r < 4)) return;
                    f++;
                  }
                  if (!Jy(lm, h())) return;
                  for (; Jy(lm, h());) {
                    if (o = $y(h(), 10), null === i) i = o;else {
                      if (0 === i) return;
                      i = 10 * i + o;
                    }
                    if (i > 255) return;
                    f++;
                  }
                  u[c] = 256 * u[c] + i, 2 != ++r && 4 !== r || c++;
                }
                if (4 !== r) return;
                break;
              }
              if (":" === h()) {
                if (f++, !h()) return;
              } else if (h()) return;
              u[c++] = t;
            } else {
              if (null !== l) return;
              f++, l = ++c;
            }
          }
          if (null !== l) for (a = c - l, c = 7; 0 !== c && a > 0;) s = u[c], u[c--] = u[l + a - 1], u[l + --a] = s;else if (8 !== c) return;
          return u;
        }(nm(e, 1, -1)), !t) return am;
        this.host = t;
      } else if (this.isSpecial()) {
        if (e = jy(e), Jy(gm, e)) return am;
        if (t = function (e) {
          var t,
            n,
            r,
            i,
            o,
            a,
            s,
            u = tm(e, ".");
          if (u.length && "" === u[u.length - 1] && u.length--, (t = u.length) > 4) return e;
          for (n = [], r = 0; r < t; r++) {
            if ("" === (i = u[r])) return e;
            if (o = 10, i.length > 1 && "0" === Wy(i, 0) && (o = Jy(fm, i) ? 16 : 8, i = nm(i, 8 === o ? 1 : 2)), "" === i) a = 0;else {
              if (!Jy(10 === o ? dm : 8 === o ? hm : pm, i)) return e;
              a = $y(i, o);
            }
            Ky(n, a);
          }
          for (r = 0; r < t; r++) if (a = n[r], r === t - 1) {
            if (a >= Hy(256, 5 - t)) return null;
          } else if (a > 255) return null;
          for (s = Yy(n), r = 0; r < n.length; r++) s += n[r] * Hy(256, 3 - r);
          return s;
        }(e), null === t) return am;
        this.host = t;
      } else {
        if (Jy(vm, e)) return am;
        for (t = "", n = Iy(e), r = 0; r < n.length; r++) t += Cm(n[r], km);
        this.host = t;
      }
    },
    cannotHaveUsernamePasswordPort: function () {
      return !this.host || this.cannotBeABaseURL || "file" === this.scheme;
    },
    includesCredentials: function () {
      return "" !== this.username || "" !== this.password;
    },
    isSpecial: function () {
      return Ty(Em, this.scheme);
    },
    shortenPath: function () {
      var e = this.path,
        t = e.length;
      !t || "file" === this.scheme && 1 === t && Tm(e[0], !0) || e.length--;
    },
    serialize: function () {
      var e = this,
        t = e.scheme,
        n = e.username,
        r = e.password,
        i = e.host,
        o = e.port,
        a = e.path,
        s = e.query,
        u = e.fragment,
        c = t + ":";
      return null !== i ? (c += "//", e.includesCredentials() && (c += n + (r ? ":" + r : "") + "@"), c += wm(i), null !== o && (c += ":" + o)) : "file" === t && (c += "//"), c += e.cannotBeABaseURL ? a[0] : a.length ? "/" + Zy(a, "/") : "", null !== s && (c += "?" + s), null !== u && (c += "#" + u), c;
    },
    setHref: function (e) {
      var t = this.parse(e);
      if (t) throw new qy(t);
      this.searchParams.update();
    },
    getOrigin: function () {
      var e = this.scheme,
        t = this.port;
      if ("blob" === e) try {
        return new Qm(e.path[0]).origin;
      } catch (UO) {
        return "null";
      }
      return "file" !== e && this.isSpecial() ? e + "://" + wm(this.host) + (null !== t ? ":" + t : "") : "null";
    },
    getProtocol: function () {
      return this.scheme + ":";
    },
    setProtocol: function (e) {
      this.parse(Ry(e) + ":", Lm);
    },
    getUsername: function () {
      return this.username;
    },
    setUsername: function (e) {
      var t = Iy(Ry(e));
      if (!this.cannotHaveUsernamePasswordPort()) {
        this.username = "";
        for (var n = 0; n < t.length; n++) this.username += Cm(t[n], Sm);
      }
    },
    getPassword: function () {
      return this.password;
    },
    setPassword: function (e) {
      var t = Iy(Ry(e));
      if (!this.cannotHaveUsernamePasswordPort()) {
        this.password = "";
        for (var n = 0; n < t.length; n++) this.password += Cm(t[n], Sm);
      }
    },
    getHost: function () {
      var e = this.host,
        t = this.port;
      return null === e ? "" : null === t ? wm(e) : wm(e) + ":" + t;
    },
    setHost: function (e) {
      this.cannotBeABaseURL || this.parse(e, zm);
    },
    getHostname: function () {
      var e = this.host;
      return null === e ? "" : wm(e);
    },
    setHostname: function (e) {
      this.cannotBeABaseURL || this.parse(e, Vm);
    },
    getPort: function () {
      var e = this.port;
      return null === e ? "" : Ry(e);
    },
    setPort: function (e) {
      this.cannotHaveUsernamePasswordPort() || ("" === (e = Ry(e)) ? this.port = null : this.parse(e, qm));
    },
    getPathname: function () {
      var e = this.path;
      return this.cannotBeABaseURL ? e[0] : e.length ? "/" + Zy(e, "/") : "";
    },
    setPathname: function (e) {
      this.cannotBeABaseURL || (this.path = [], this.parse(e, Wm));
    },
    getSearch: function () {
      var e = this.query;
      return e ? "?" + e : "";
    },
    setSearch: function (e) {
      "" === (e = Ry(e)) ? this.query = null : ("?" === Wy(e, 0) && (e = nm(e, 1)), this.query = "", this.parse(e, Xm)), this.searchParams.update();
    },
    getSearchParams: function () {
      return this.searchParams.facade;
    },
    getHash: function () {
      var e = this.fragment;
      return e ? "#" + e : "";
    },
    setHash: function (e) {
      "" !== (e = Ry(e)) ? ("#" === Wy(e, 0) && (e = nm(e, 1)), this.fragment = "", this.parse(e, Ym)) : this.fragment = null;
    },
    update: function () {
      this.query = this.searchParams.serialize() || null;
    }
  };
  var Qm = function (e) {
      var t = Ey(this, eb),
        n = _y(arguments.length, 1) > 1 ? arguments[1] : void 0,
        r = My(t, new Km(e, !1, n));
      by || (t.href = r.serialize(), t.origin = r.getOrigin(), t.protocol = r.getProtocol(), t.username = r.getUsername(), t.password = r.getPassword(), t.host = r.getHost(), t.hostname = r.getHostname(), t.port = r.getPort(), t.pathname = r.getPathname(), t.search = r.getSearch(), t.searchParams = r.getSearchParams(), t.hash = r.getHash());
    },
    eb = Qm.prototype,
    tb = function (e, t) {
      return {
        get: function () {
          return Uy(this)[e]();
        },
        set: t && function (e) {
          return Uy(this)[t](e);
        },
        configurable: !0,
        enumerable: !0
      };
    };
  if (by && (Cy(eb, "href", tb("serialize", "setHref")), Cy(eb, "origin", tb("getOrigin")), Cy(eb, "protocol", tb("getProtocol", "setProtocol")), Cy(eb, "username", tb("getUsername", "setUsername")), Cy(eb, "password", tb("getPassword", "setPassword")), Cy(eb, "host", tb("getHost", "setHost")), Cy(eb, "hostname", tb("getHostname", "setHostname")), Cy(eb, "port", tb("getPort", "setPort")), Cy(eb, "pathname", tb("getPathname", "setPathname")), Cy(eb, "search", tb("getSearch", "setSearch")), Cy(eb, "searchParams", tb("getSearchParams")), Cy(eb, "hash", tb("getHash", "setHash"))), Sy(eb, "toJSON", function () {
    return Uy(this).serialize();
  }, {
    enumerable: !0
  }), Sy(eb, "toString", function () {
    return Uy(this).serialize();
  }, {
    enumerable: !0
  }), Vy) {
    var nb = Vy.createObjectURL,
      rb = Vy.revokeObjectURL;
    nb && Sy(Qm, "createObjectURL", Py(nb, Vy)), rb && Sy(Qm, "revokeObjectURL", Py(rb, Vy));
  }
  By(Qm, "URL"), my({
    global: !0,
    constructor: !0,
    forced: !wy,
    sham: !by
  }, {
    URL: Qm
  });
  var ib = _;
  Si({
    target: "URL",
    proto: !0,
    enumerable: !0
  }, {
    toJSON: function () {
      return ib(URL.prototype.toString, this);
    }
  });
  var ob = new WeakMap(),
    ab = function () {
      return d(function e(t, n) {
        var i = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : function (e) {
          return atob(e);
        };
        f(this, e), S(this, ob, void 0), this.release = t, this.scriptSource = n, this.decrypt = i, r(ob, this, this.getCdnUrl());
      }, [{
        key: "isActive",
        value: function () {
          var e = this.decrypt("c29saWRnYXRl"),
            t = window.location.toString(),
            n = this.scriptSource.includes(e),
            r = t.includes("payment-form/src/sdk/index.html") && !t.includes("nobrand");
          return n || r;
        }
      }, {
        key: "getIsBrandedLogoParameterName",
        value: function () {
          return this.decrypt("aXNTb2xpZExvZ29WaXNpYmxl");
        }
      }, {
        key: "getSentryDSN",
        value: function () {
          return this.decrypt("aHR0cHM6Ly8zMTFjNmRlNjlmMTE5MmQyNzE2OGM0MDdlZmI2ZTFkMkBzbnRyLnNvbGlkZ2F0ZS1kZXYuY29tLzQ=");
        }
      }, {
        key: "getTrackingUrl",
        value: function () {
          return this.decrypt("aHR0cHM6Ly90cmFjay1leHQuc29saWRnYXRlLmNvbS8=");
        }
      }, {
        key: "getPaymentFormUrl",
        value: function () {
          return this.decrypt("aHR0cHM6Ly9mb3JtLXYyLnNvbGlkZ2F0ZS5jb20=");
        }
      }, {
        key: "getAltGateBaseUrl",
        value: function () {
          return this.decrypt("aHR0cHM6Ly9nYXRlLnNvbGlkZ2F0ZS5jb20v");
        }
      }, {
        key: "getCdnList",
        value: function () {
          return [this.getCdnUrl()];
        }
      }, {
        key: "getSdkInitType",
        value: function () {
          return window[this.decrypt("X19TT0xJREdBVEVfUFJJVkFURV9fU0RLX0lOSVRfVFlQRQ==")];
        }
      }, {
        key: "getDefaultFormId",
        value: function () {
          return this.decrypt("c29saWQtcGF5bWVudC1mb3JtLWNvbnRhaW5lcg==");
        }
      }, {
        key: "getIframeId",
        value: function () {
          return this.decrypt("c29saWQtcGF5bWVudC1mb3JtLWlmcmFtZQ==");
        }
      }, {
        key: "getIframeUrl",
        value: function () {
          return "".concat(this.decrypt("aHR0cHM6Ly9mb3JtLXYyLnNvbGlkZ2F0ZS5jb20="), "/version/").concat(this.release);
        }
      }, {
        key: "getCdnUrl",
        value: function () {
          return n(ob, this) || this.scriptSource && r(ob, this, new URL(this.scriptSource || "").hostname), n(ob, this);
        }
      }]);
    }(),
    sb = A,
    ub = O.RegExp,
    cb = sb(function () {
      var e = ub("a", "y");
      return e.lastIndex = 2, null !== e.exec("abcd");
    }),
    lb = cb || sb(function () {
      return !ub("a", "y").sticky;
    }),
    fb = {
      BROKEN_CARET: cb || sb(function () {
        var e = ub("^r", "gy");
        return e.lastIndex = 2, null !== e.exec("str");
      }),
      MISSED_STICKY: lb,
      UNSUPPORTED_Y: cb
    },
    hb = A,
    db = O.RegExp,
    pb = hb(function () {
      var e = db(".", "s");
      return !(e.dotAll && e.test("\n") && "s" === e.flags);
    }),
    gb = A,
    vb = O.RegExp,
    yb = gb(function () {
      var e = vb("(?<a>b)", "g");
      return "b" !== e.exec("b").groups.a || "bc" !== "b".replace(e, "$<a>c");
    }),
    mb = _,
    bb = W,
    wb = Kf,
    kb = eh,
    Pb = fb,
    xb = Rl,
    Sb = Qn.get,
    Cb = pb,
    Eb = yb,
    Tb = ot("native-string-replace", String.prototype.replace),
    Ob = RegExp.prototype.exec,
    Ib = Ob,
    Ab = bb("".charAt),
    Lb = bb("".indexOf),
    jb = bb("".replace),
    Rb = bb("".slice),
    Bb = function () {
      var e = /a/,
        t = /b*/g;
      return mb(Ob, e, "a"), mb(Ob, t, "a"), 0 !== e.lastIndex || 0 !== t.lastIndex;
    }(),
    _b = Pb.BROKEN_CARET,
    Nb = void 0 !== /()??/.exec("")[1];
  (Bb || Nb || _b || Cb || Eb) && (Ib = function (e) {
    var t,
      n,
      r,
      i,
      o,
      a,
      s,
      u = this,
      c = Sb(u),
      l = wb(e),
      f = c.raw;
    if (f) return f.lastIndex = u.lastIndex, t = mb(Ib, f, l), u.lastIndex = f.lastIndex, t;
    var h = c.groups,
      d = _b && u.sticky,
      p = mb(kb, u),
      g = u.source,
      v = 0,
      y = l;
    if (d && (p = jb(p, "y", ""), -1 === Lb(p, "g") && (p += "g"), y = Rb(l, u.lastIndex), u.lastIndex > 0 && (!u.multiline || u.multiline && "\n" !== Ab(l, u.lastIndex - 1)) && (g = "(?: " + g + ")", y = " " + y, v++), n = new RegExp("^(?:" + g + ")", p)), Nb && (n = new RegExp("^" + g + "$(?!\\s)", p)), Bb && (r = u.lastIndex), i = mb(Ob, d ? n : u, y), d ? i ? (i.input = Rb(i.input, v), i[0] = Rb(i[0], v), i.index = u.lastIndex, u.lastIndex += i[0].length) : u.lastIndex = 0 : Bb && i && (u.lastIndex = u.global ? i.index + i[0].length : r), Nb && i && i.length > 1 && mb(Tb, i[0], n, function () {
      for (o = 1; o < arguments.length - 2; o++) void 0 === arguments[o] && (i[o] = void 0);
    }), i && h) for (i.groups = a = xb(null), o = 0; o < h.length; o++) a[(s = h[o])[0]] = i[s[1]];
    return i;
  });
  var Fb = Ib;
  Si({
    target: "RegExp",
    proto: !0,
    forced: /./.exec !== Fb
  }, {
    exec: Fb
  });
  var Mb = _,
    Ub = Pr,
    Db = Fb,
    zb = A,
    Vb = Ct,
    qb = mn,
    $b = Vb("species"),
    Gb = RegExp.prototype,
    Hb = function (e, t, n, r) {
      var i = Vb(e),
        o = !zb(function () {
          var t = {};
          return t[i] = function () {
            return 7;
          }, 7 !== ""[e](t);
        }),
        a = o && !zb(function () {
          var t = !1,
            n = /a/;
          return "split" === e && ((n = {}).constructor = {}, n.constructor[$b] = function () {
            return n;
          }, n.flags = "", n[i] = /./[i]), n.exec = function () {
            return t = !0, null;
          }, n[i](""), !t;
        });
      if (!o || !a || n) {
        var s = /./[i],
          u = t(i, ""[e], function (e, t, n, r, i) {
            var a = t.exec;
            return a === Db || a === Gb.exec ? o && !i ? {
              done: !0,
              value: Mb(s, t, n, r)
            } : {
              done: !0,
              value: Mb(e, n, t, r)
            } : {
              done: !1
            };
          });
        Ub(String.prototype, e, u[0]), Ub(Gb, i, u[1]);
      }
      r && qb(Gb[i], "sham", !0);
    },
    Wb = Uh.charAt,
    Jb = function (e, t, n) {
      return t + (n ? Wb(e, t).length : 1);
    },
    Zb = W,
    Xb = ut,
    Yb = Math.floor,
    Kb = Zb("".charAt),
    Qb = Zb("".replace),
    ew = Zb("".slice),
    tw = /\$([$&'`]|\d{1,2}|<[^>]*>)/g,
    nw = /\$([$&'`]|\d{1,2})/g,
    rw = _,
    iw = rn,
    ow = fe,
    aw = Y,
    sw = Fb,
    uw = TypeError,
    cw = function (e, t) {
      var n = e.exec;
      if (ow(n)) {
        var r = rw(n, e, t);
        return null !== r && iw(r), r;
      }
      if ("RegExp" === aw(e)) return rw(sw, e, t);
      throw new uw("RegExp#exec called on incompatible receiver");
    },
    lw = va,
    fw = _,
    hw = W,
    dw = Hb,
    pw = A,
    gw = rn,
    vw = fe,
    yw = re,
    mw = Tr,
    bw = Br,
    ww = Kf,
    kw = ae,
    Pw = Jb,
    xw = $e,
    Sw = function (e, t, n, r, i, o) {
      var a = n + e.length,
        s = r.length,
        u = nw;
      return void 0 !== i && (i = Xb(i), u = tw), Qb(o, u, function (o, u) {
        var c;
        switch (Kb(u, 0)) {
          case "$":
            return "$";
          case "&":
            return e;
          case "`":
            return ew(t, 0, n);
          case "'":
            return ew(t, a);
          case "<":
            c = i[ew(u, 1, -1)];
            break;
          default:
            var l = +u;
            if (0 === l) return o;
            if (l > s) {
              var f = Yb(l / 10);
              return 0 === f ? o : f <= s ? void 0 === r[f - 1] ? Kb(u, 1) : r[f - 1] + Kb(u, 1) : o;
            }
            c = r[l - 1];
        }
        return void 0 === c ? "" : c;
      });
    },
    Cw = cw,
    Ew = Ct("replace"),
    Tw = Math.max,
    Ow = Math.min,
    Iw = hw([].concat),
    Aw = hw([].push),
    Lw = hw("".indexOf),
    jw = hw("".slice),
    Rw = function (e) {
      return void 0 === e ? e : String(e);
    },
    Bw = function () {
      return "$0" === "a".replace(/./, "$0");
    }(),
    _w = function () {
      return !!/./[Ew] && "" === /./[Ew]("a", "$0");
    }();
  dw("replace", function (e, t, n) {
    var r = _w ? "$" : "$0";
    return [function (e, n) {
      var r = kw(this),
        i = yw(e) ? void 0 : xw(e, Ew);
      return i ? fw(i, e, r, n) : fw(t, ww(r), e, n);
    }, function (e, i) {
      var o = gw(this),
        a = ww(e);
      if ("string" == typeof i && -1 === Lw(i, r) && -1 === Lw(i, "$<")) {
        var s = n(t, o, a, i);
        if (s.done) return s.value;
      }
      var u = vw(i);
      u || (i = ww(i));
      var c,
        l = o.global;
      l && (c = o.unicode, o.lastIndex = 0);
      for (var f, h = []; null !== (f = Cw(o, a)) && (Aw(h, f), l);) {
        "" === ww(f[0]) && (o.lastIndex = Pw(a, bw(o.lastIndex), c));
      }
      for (var d = "", p = 0, g = 0; g < h.length; g++) {
        for (var v, y = ww((f = h[g])[0]), m = Tw(Ow(mw(f.index), a.length), 0), b = [], w = 1; w < f.length; w++) Aw(b, Rw(f[w]));
        var k = f.groups;
        if (u) {
          var P = Iw([y], b, m, a);
          void 0 !== k && Aw(P, k), v = ww(lw(i, void 0, P));
        } else v = Sw(y, a, m, b, k, i);
        m >= p && (d += jw(a, p, m) + v, p = m + y.length);
      }
      return d + jw(a, p);
    }];
  }, !!pw(function () {
    var e = /./;
    return e.exec = function () {
      var e = [];
      return e.groups = {
        a: "7"
      }, e;
    }, "7" !== "".replace(e, "$<a>");
  }) || !Bw || _w);
  var Nw = new WeakMap(),
    Fw = function () {
      return d(function e(t, n) {
        var i = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : function (e) {
          return atob(e);
        };
        f(this, e), S(this, Nw, void 0), this.release = t, this.scriptSource = n, this.decrypt = i, r(Nw, this, new ab(t, n, i));
      }, [{
        key: "getIsBrandedLogoParameterName",
        value: function () {
          return n(Nw, this).getIsBrandedLogoParameterName();
        }
      }, {
        key: "getSentryDSN",
        value: function () {
          var e = n(Nw, this).getSentryDSN(),
            t = n(Nw, this).getCdnUrl().split(".")[1];
          return e.replace(this.decrypt("c29saWRnYXRlLWRldg=="), t);
        }
      }, {
        key: "getTrackingUrl",
        value: function () {
          return this.decrypt("aHR0cHM6Ly90cmFjay5jaGFyZ2UtYXV0aC5jb20v");
        }
      }, {
        key: "getPaymentFormUrl",
        value: function () {
          return this.decrypt("aHR0cHM6Ly9mb3JtLXYyLmNoYXJnZS1hdXRoLmNvbQ==");
        }
      }, {
        key: "getAltGateBaseUrl",
        value: function () {
          return this.decrypt("aHR0cHM6Ly9nYXRlLmNoYXJnZS1hdXRoLmNvbS8=");
        }
      }, {
        key: "getCdnList",
        value: function () {
          return n(Nw, this).getCdnList();
        }
      }, {
        key: "getSdkInitType",
        value: function () {
          return n(Nw, this).getSdkInitType();
        }
      }, {
        key: "getDefaultFormId",
        value: function () {
          return "none";
        }
      }, {
        key: "getIframeId",
        value: function () {
          return "payment-form-iframe";
        }
      }, {
        key: "getIframeUrl",
        value: function () {
          return "".concat(this.decrypt("aHR0cHM6Ly9mb3JtLXYyLmNoYXJnZS1hdXRoLmNvbQ=="), "/version/").concat(this.release);
        }
      }]);
    }(),
    Mw = function () {
      return d(function e() {
        f(this, e);
      }, [{
        key: "getBranding",
        value: function (e, t) {
          var n = new ab(e, t);
          return n.isActive() ? n : new Fw(e, t);
        }
      }]);
    }(),
    Uw = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, [e])).name = "BootstrapError", r;
      }
      return g(n, e), d(n);
    }(m(Error)),
    Dw = Si,
    zw = Qd.find,
    Vw = Ul,
    qw = "find",
    $w = !0;
  qw in [] && Array(1)[qw](function () {
    $w = !1;
  }), Dw({
    target: "Array",
    proto: !0,
    forced: $w
  }, {
    find: function (e) {
      return zw(this, e, arguments.length > 1 ? arguments[1] : void 0);
    }
  }), Vw(qw);
  var Gw = A,
    Hw = function (e, t) {
      var n = [][e];
      return !!n && Gw(function () {
        n.call(null, t || function () {
          return 1;
        }, 1);
      });
    },
    Ww = Si,
    Jw = zr.indexOf,
    Zw = Hw,
    Xw = ba([].indexOf),
    Yw = !!Xw && 1 / Xw([1], 1, -0) < 0;
  Ww({
    target: "Array",
    proto: !0,
    forced: Yw || !Zw("indexOf")
  }, {
    indexOf: function (e) {
      var t = arguments.length > 1 ? arguments[1] : void 0;
      return Yw ? Xw(this, e, t) || 0 : Jw(this, e, t);
    }
  });
  var Kw = ut,
    Qw = Rt;
  Si({
    target: "Date",
    proto: !0,
    arity: 1,
    forced: A(function () {
      return null !== new Date(NaN).toJSON() || 1 !== Date.prototype.toJSON.call({
        toISOString: function () {
          return 1;
        }
      });
    })
  }, {
    toJSON: function (e) {
      var t = Kw(this),
        n = Qw(t, "number");
      return "number" != typeof n || isFinite(n) ? t.toISOString() : null;
    }
  });
  var ek = L,
    tk = A,
    nk = W,
    rk = Ql,
    ik = hl,
    ok = ce,
    ak = nk(N.f),
    sk = nk([].push),
    uk = ek && tk(function () {
      var e = Object.create(null);
      return e[2] = 2, !ak(e, 2);
    }),
    ck = function (e) {
      return function (t) {
        for (var n, r = ok(t), i = ik(r), o = uk && null === rk(r), a = i.length, s = 0, u = []; a > s;) n = i[s++], ek && !(o ? n in r : ak(r, n)) || sk(u, e ? [n, r[n]] : r[n]);
        return u;
      };
    },
    lk = {
      entries: ck(!0),
      values: ck(!1)
    },
    fk = lk.entries;
  Si({
    target: "Object",
    stat: !0
  }, {
    entries: function (e) {
      return fk(e);
    }
  });
  var hk = Qd.forEach,
    dk = Hw("forEach") ? [].forEach : function (e) {
      return hk(this, e, arguments.length > 1 ? arguments[1] : void 0);
    },
    pk = O,
    gk = Gp,
    vk = Jp,
    yk = dk,
    mk = mn,
    bk = function (e) {
      if (e && e.forEach !== yk) try {
        mk(e, "forEach", yk);
      } catch (UO) {
        e.forEach = yk;
      }
    };
  for (var wk in gk) gk[wk] && bk(pk[wk] && pk[wk].prototype);
  bk(vk);
  var kk = d(function e() {
      f(this, e);
    }),
    Pk = function (e) {
      return e.Ok = "ok", e.DeadlineExceeded = "deadline_exceeded", e.Unauthenticated = "unauthenticated", e.PermissionDenied = "permission_denied", e.NotFound = "not_found", e.ResourceExhausted = "resource_exhausted", e.InvalidArgument = "invalid_argument", e.Unimplemented = "unimplemented", e.Unavailable = "unavailable", e.InternalError = "internal_error", e.UnknownError = "unknown_error", e.Cancelled = "cancelled", e.AlreadyExists = "already_exists", e.FailedPrecondition = "failed_precondition", e.Aborted = "aborted", e.OutOfRange = "out_of_range", e.DataLoss = "data_loss", e;
    }(Pk || {}),
    xk = Qd.map;
  Si({
    target: "Array",
    proto: !0,
    forced: !lo("map")
  }, {
    map: function (e) {
      return xk(this, e, arguments.length > 1 ? arguments[1] : void 0);
    }
  });
  var Sk = Si,
    Ck = Ei,
    Ek = Qi,
    Tk = de,
    Ok = Lr,
    Ik = Nr,
    Ak = ce,
    Lk = Li,
    jk = Ct,
    Rk = Ca,
    Bk = lo("slice"),
    _k = jk("species"),
    Nk = Array,
    Fk = Math.max;
  Sk({
    target: "Array",
    proto: !0,
    forced: !Bk
  }, {
    slice: function (e, t) {
      var n,
        r,
        i,
        o = Ak(this),
        a = Ik(o),
        s = Ok(e, a),
        u = Ok(void 0 === t ? a : t, a);
      if (Ck(o) && (n = o.constructor, (Ek(n) && (n === Nk || Ck(n.prototype)) || Tk(n) && null === (n = n[_k])) && (n = void 0), n === Nk || void 0 === n)) return Rk(o, s, u);
      for (r = new (void 0 === n ? Nk : n)(Fk(u - s, 0)), i = 0; s < u; s++, i++) s in o && Lk(r, i, o[s]);
      return r.length = i, r;
    }
  });
  var Mk = _,
    Uk = rn,
    Dk = re,
    zk = Br,
    Vk = Kf,
    qk = ae,
    $k = $e,
    Gk = Jb,
    Hk = cw;
  Hb("match", function (e, t, n) {
    return [function (t) {
      var n = qk(this),
        r = Dk(t) ? void 0 : $k(t, e);
      return r ? Mk(r, t, n) : new RegExp(t)[e](Vk(n));
    }, function (e) {
      var r = Uk(this),
        i = Vk(e),
        o = n(t, r, i);
      if (o.done) return o.value;
      if (!r.global) return Hk(r, i);
      var a = r.unicode;
      r.lastIndex = 0;
      for (var s, u = [], c = 0; null !== (s = Hk(r, i));) {
        var l = Vk(s[0]);
        u[c] = l, "" === l && (r.lastIndex = Gk(i, zk(r.lastIndex), a)), c++;
      }
      return 0 === c ? null : u;
    }];
  });
  var Wk,
    Jk = Qd.filter;
  function Zk() {
    return function () {
      return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (e) {
        var t = 16 * Math.random() | 0;
        return ("x" === e ? t : 3 & t | 8).toString(16);
      });
    }().split("").filter(function (e) {
      return "-" !== e;
    }).join("");
  }
  function Xk() {
    return Zk().slice(0, 16);
  }
  function Yk() {
    return Date.now() / 1e3;
  }
  Si({
    target: "Array",
    proto: !0,
    forced: !lo("filter")
  }, {
    filter: function (e) {
      return Jk(this, e, arguments.length > 1 ? arguments[1] : void 0);
    }
  });
  var Kk = function () {
      return d(function e(t) {
        var n = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : "function";
        f(this, e), this.name = t, this.op = n, this.startTimestamp = Yk(), this.status = "", this.id = Xk(), this.endTimestamp = 0;
      }, [{
        key: "isFinished",
        value: function () {
          return !!this.endTimestamp;
        }
      }, {
        key: "finish",
        value: function () {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : Pk.Ok;
          this.endTimestamp = Yk(), this.status = e;
        }
      }]);
    }(),
    Qk = function (e) {
      function n(e, r) {
        var i;
        return f(this, n), (i = t(this, n, [e])).onceFinish = r, i.spans = [], i.traceId = Zk(), i.id = Zk(), i;
      }
      return g(n, e), d(n, [{
        key: "getLastSpanId",
        value: function () {
          var e = this.getLastSpan();
          return e ? e.id : Xk();
        }
      }, {
        key: "addSpan",
        value: function (e, t) {
          var n = new Kk(e, t);
          return this.spans.push(n), n;
        }
      }, {
        key: "finish",
        value: function () {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : Pk.Ok,
            t = this.isFinished(),
            r = this.getLastSpan();
          b(v(n.prototype), "finish", this).call(this, e), r && !r.isFinished() && r.finish(e), t || this.onceFinish();
        }
      }, {
        key: "getLastSpan",
        value: function () {
          return this.spans[this.spans.length - 1];
        }
      }]);
    }(Kk),
    eP = function (e) {
      function n(e, r, i, o) {
        var a;
        return f(this, n), (a = t(this, n)).environment = e, a.releaseVersion = r, a.envelopeUrl = i, a.sampleRate = o, a.currentTrace = null, a;
      }
      return g(n, e), d(n, [{
        key: "trace",
        value: function (e) {
          var t = this,
            n = new Qk(e, function () {
              t.sendTransaction(n), t.currentTrace === n && (t.currentTrace = null);
            });
          return this.currentTrace = n, this.currentTrace;
        }
      }, {
        key: "sendTransaction",
        value: function (e) {
          if (this.allowBySampleRate()) {
            var t = {
                transaction: e.name,
                type: "transaction",
                release: this.releaseVersion,
                platform: "javascript",
                environment: this.environment,
                event_id: e.id,
                timestamp: e.endTimestamp,
                start_timestamp: e.startTimestamp,
                contexts: {
                  trace: {
                    op: e.op,
                    trace_id: e.traceId,
                    span_id: Xk(),
                    status: e.status
                  }
                },
                spans: e.spans.map(function (t) {
                  return {
                    span_id: t.id.slice(0, 16),
                    op: t.op,
                    description: t.name,
                    timestamp: t.endTimestamp,
                    start_timestamp: t.startTimestamp,
                    status: t.status,
                    trace_id: e.traceId
                  };
                }),
                sdk: {
                  name: "payments.tiny-sdk",
                  version: "2.0.0"
                }
              },
              n = JSON.stringify({
                event_id: t.event_id,
                sample_rate: 1,
                sent_at: new Date().toISOString(),
                sdk: {
                  name: "payments.tiny-sdk",
                  version: "2.0.0"
                }
              });
            n += "\n", n += JSON.stringify({
              type: "transaction"
            }), n += "\n", n += JSON.stringify(t), n += "\n", this.request(n, this.envelopeUrl);
          }
        }
      }, {
        key: "allowBySampleRate",
        value: function () {
          return Math.random() < this.sampleRate;
        }
      }, {
        key: "request",
        value: function (e, t) {
          if (t && e) {
            var n = new XMLHttpRequest();
            n.open("post", t, !0), n.send(e);
          }
        }
      }], [{
        key: "parseDsn",
        value: function (e) {
          if (!e) return {
            storeUrl: "",
            envelopeUrl: "",
            publicKey: ""
          };
          var t = w(n.DsnRegex.exec(e).slice(1), 6),
            r = t[0],
            i = t[1],
            o = t[3],
            a = "",
            s = t[5],
            u = s.split("/");
          if (u.length > 1 && (a = u.slice(0, -1).join("/"), s = u.pop()), s) {
            var c = s.match(/^\d+/);
            c && (s = c[0]);
          }
          return {
            publicKey: i || "",
            storeUrl: "".concat(r, "://").concat(o).concat(a, "/api/").concat(s, "/store/?sentry_version=7&sentry_key=").concat(i, "&sentry_debug=true"),
            envelopeUrl: "".concat(r, "://").concat(o).concat(a, "/api/").concat(s, "/envelope/?sentry_version=7&sentry_key=").concat(i)
          };
        }
      }]);
    }(kk);
  (Wk = eP).sentryId = Zk, Wk.DsnRegex = /^(?:(\w+):)\/\/(?:(\w+)(?::(\w+))?@)([\w.-]+)(?::(\d+))?\/(.+)/;
  var tP = "?",
    nP = /^\s*at (?:(.*?) ?\()?((?:file|https?|blob|chrome-extension|address|native|eval|webpack|<anonymous>|[-a-z]+:|.*bundle|\/).*?)(?::(\d+))?(?::(\d+))?\)?\s*$/i,
    rP = /^\s*(.*?)(?:\((.*?)\))?(?:^|@)?((?:file|https?|blob|chrome|webpack|resource|moz-extension|capacitor).*?:\/.*?|\[native code\]|[^@]*(?:bundle|\d+\.js)|\/[\w\-. /=]+)(?::(\d+))?(?::(\d+))?\s*$/i,
    iP = /^\s*at (?:((?:\[object object\])?.+) )?\(?((?:file|ms-appx|https?|webpack|blob):.*?):(\d+)(?::(\d+))?\)?\s*$/i,
    oP = /(\S+) line (\d+)(?: > eval line \d+)* > eval/i,
    aP = /\((\S*)(?::(\d+))(?::(\d+))\)/,
    sP = /Minified React error #\d+;/i;
  function uP(e) {
    var t = null,
      n = 0;
    e && ("number" == typeof e.framesToPop ? n = e.framesToPop : sP.test(e.message) && (n = 1));
    try {
      if (t = function (e) {
        if (!e || !e.stacktrace) return null;
        for (var t, n = e.stacktrace, r = / line (\d+).*script (?:in )?(\S+)(?:: in function (\S+))?$/i, i = / line (\d+), column (\d+)\s*(?:in (?:<anonymous function: ([^>]+)>|([^)]+))\((.*)\))? in (.*):\s*$/i, o = n.split("\n"), a = [], s = 0; s < o.length; s += 2) {
          var u = null;
          (t = r.exec(o[s])) ? u = {
            url: t[2],
            func: t[3],
            args: [],
            line: +t[1],
            column: null
          } : (t = i.exec(o[s])) && (u = {
            url: t[6],
            func: t[3] || t[4],
            args: t[5] ? t[5].split(",") : [],
            line: +t[1],
            column: +t[2]
          }), u && (!u.func && u.line && (u.func = tP), a.push(u));
        }
        if (!a.length) return null;
        return {
          message: lP(e),
          name: e.name,
          stack: a
        };
      }(e), t) return cP(t, n);
    } catch (r) {}
    try {
      if (t = function (e) {
        if (!e || !e.stack) return null;
        for (var t, n, r, i = [], o = e.stack.split("\n"), a = 0; a < o.length; ++a) {
          if (n = nP.exec(o[a])) {
            var s = n[2] && 0 === n[2].indexOf("native");
            n[2] && 0 === n[2].indexOf("eval") && (t = aP.exec(n[2])) && (n[2] = t[1], n[3] = t[2], n[4] = t[3]);
            var u = n[2] && 0 === n[2].indexOf("address at ") ? n[2].substr(11) : n[2],
              c = n[1] || tP,
              l = -1 !== c.indexOf("safari-extension"),
              f = -1 !== c.indexOf("safari-web-extension");
            (l || f) && (c = -1 !== c.indexOf("@") ? c.split("@")[0] : tP, u = l ? "safari-extension:".concat(u) : "safari-web-extension:".concat(u)), r = {
              url: u,
              func: c,
              args: s ? [n[2]] : [],
              line: n[3] ? +n[3] : null,
              column: n[4] ? +n[4] : null
            };
          } else if (n = iP.exec(o[a])) r = {
            url: n[2],
            func: n[1] || tP,
            args: [],
            line: +n[3],
            column: n[4] ? +n[4] : null
          };else {
            if (!(n = rP.exec(o[a]))) continue;
            n[3] && n[3].indexOf(" > eval") > -1 && (t = oP.exec(n[3])) ? (n[1] = n[1] || "eval", n[3] = t[1], n[4] = t[2], n[5] = "") : 0 !== a || n[5] || void 0 === e.columnNumber || (i[0].column = e.columnNumber + 1), r = {
              url: n[3],
              func: n[1] || tP,
              args: n[2] ? n[2].split(",") : [],
              line: n[4] ? +n[4] : null,
              column: n[5] ? +n[5] : null
            };
          }
          !r.func && r.line && (r.func = tP), i.push(r);
        }
        if (!i.length) return null;
        return {
          message: lP(e),
          name: e.name,
          stack: i
        };
      }(e), t) return cP(t, n);
    } catch (r) {}
    return {
      message: lP(e),
      name: e && e.name,
      stack: [],
      failed: !0
    };
  }
  function cP(e, t) {
    try {
      return a(a({}, e), {}, {
        stack: e.stack.slice(t)
      });
    } catch (n) {
      return e;
    }
  }
  function lP(e) {
    var t = e && e.message;
    return t ? t.error && "string" == typeof t.error.message ? t.error.message : t : "No error message";
  }
  var fP = Si,
    hP = Ei,
    dP = W([].reverse),
    pP = [1, 2];
  fP({
    target: "Array",
    proto: !0,
    forced: String(pP) === String(pP.reverse())
  }, {
    reverse: function () {
      return hP(this) && (this.length = this.length), dP(this);
    }
  });
  var gP = 50;
  function vP(e) {
    var t = function (e) {
        if (!e || !e.length) return [];
        var t = e,
          n = t[0].func || "",
          r = t[t.length - 1].func || "";
        return -1 === n.indexOf("captureMessage") && -1 === n.indexOf("captureException") || (t = t.slice(1)), -1 !== r.indexOf("sentryWrapped") && (t = t.slice(0, -1)), t.slice(0, gP).map(function (e) {
          return {
            colno: null === e.column ? void 0 : e.column,
            filename: e.url || t[0].url,
            function: e.func || "?",
            in_app: !0,
            lineno: null === e.line ? void 0 : e.line
          };
        }).reverse();
      }(e.stack),
      n = {
        type: e.name,
        value: e.message
      };
    return t && t.length && (n.stacktrace = {
      frames: t
    }), void 0 === n.type && "" === n.value && (n.value = "Unrecoverable error caught"), n;
  }
  function yP() {
    return Date.now() / 1e3;
  }
  var mP = function () {
      return d(function e(t, n, r, i) {
        f(this, e), this.releaseVersion = n, this.environment = r, this.dsn = "", this.envelopeUrl = "", this.publicKey = "", this.init(t), this.tracer = new eP(r, n, this.envelopeUrl, i);
      }, [{
        key: "warning",
        value: function (e) {
          var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {};
          this.log(e, t, "warning");
        }
      }, {
        key: "error",
        value: function (e) {
          var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {};
          this.log(e, t, "error");
        }
      }, {
        key: "debug",
        value: function (e) {
          console.debug(e);
        }
      }, {
        key: "trace",
        value: function (e) {
          return this.tracer.trace(e);
        }
      }, {
        key: "withinContext",
        value: function (e, t) {
          var n = this.tracer.currentTrace;
          this.tracer.currentTrace = e, t(), this.tracer.currentTrace = n;
        }
      }, {
        key: "log",
        value: function (e) {
          var t,
            n,
            r,
            i = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {},
            o = arguments.length > 2 ? arguments[2] : void 0;
          this.dsn && this.publicKey || console.error(e, i);
          var a = eP.sentryId(),
            s = this.parseException(e),
            u = s.exception,
            c = s.fileName,
            l = s.debugId,
            f = {
              event_id: a,
              sent_at: new Date().toISOString,
              sdk: {
                name: "payments.tiny-sdk",
                version: "2.0.0"
              },
              trace: {
                environment: this.environment,
                release: this.releaseVersion,
                public_key: this.publicKey,
                trace_id: null === (t = this.tracer.currentTrace) || void 0 === t ? void 0 : t.id,
                sample_rate: "1",
                transaction: null === (n = this.tracer.currentTrace) || void 0 === n ? void 0 : n.name,
                sampled: "true"
              }
            },
            h = {
              exception: {
                values: [u]
              },
              level: o,
              event_id: a,
              platform: "javascript",
              request: this.getRequest(),
              timestamp: yP(),
              environment: this.environment,
              release: this.releaseVersion,
              sdk: {
                name: "payments.tiny-sdk",
                version: "2.0.0"
              },
              transaction: null === (r = this.tracer.currentTrace) || void 0 === r ? void 0 : r.name,
              debug_meta: {
                images: [{
                  type: "sourcemap",
                  code_file: c,
                  debug_id: l
                }]
              },
              contexts: void 0
            };
          this.tracer.currentTrace && (h.contexts = {
            trace: {
              trace_id: this.tracer.currentTrace.traceId,
              span_id: this.tracer.currentTrace.getLastSpanId()
            }
          });
          var d = JSON.stringify(f);
          d += "\n", d += JSON.stringify({
            type: "event"
          }), d += "\n", d += JSON.stringify(h), d += "\n", this.request(d, this.envelopeUrl);
        }
      }, {
        key: "parseException",
        value: function (e) {
          var t,
            n,
            r = vP(uP(e)),
            i = (null === (t = r.stacktrace) || void 0 === t ? void 0 : t.frames) && (null === (n = r.stacktrace) || void 0 === n || null === (n = n.frames[0]) || void 0 === n ? void 0 : n.filename) || "",
            o = "";
          try {
            var a = Object.entries(window._sentryDebugIds),
              s = a.find(function (e) {
                return w(e, 1)[0].indexOf(i) > -1;
              }) || ["", ""];
            if (!(o = w(s, 2)[1])) {
              var u = a.find(function (e) {
                return w(e, 1)[0].indexOf("form") > -1;
              }) || ["", ""];
              o = w(u, 2)[1];
            }
          } catch (c) {
            o = "";
          }
          return {
            exception: r,
            fileName: i,
            debugId: o
          };
        }
      }, {
        key: "init",
        value: function (e) {
          this.dsn = e;
          var t = eP.parseDsn(e),
            n = t.envelopeUrl,
            r = t.publicKey;
          this.envelopeUrl = n, this.publicKey = r;
        }
      }, {
        key: "request",
        value: function (e, t) {
          if (t && e) {
            var n = new XMLHttpRequest();
            n.open("post", t, !0), n.send(e);
          }
        }
      }, {
        key: "getRequest",
        value: function () {
          return {
            url: window.location.href,
            headers: {
              "User-Agent": navigator.userAgent
            }
          };
        }
      }]);
    }(),
    bP = function (e) {
      return e.Mounted = "mounted", e.ProviderToken = "_providerToken", e.UpdatePaymentIntent = "updateInitPayment", e.FormInitialization = "initialization", e.SetPaymentIntent = "processor.message.setPaymentIntent", e.SetResignIntent = "processor.message.setResignIntent", e.BrowserWindowLocked = "processor.message.browserWindowLocked", e.SubmitRequest = "processor.message.submitRequest", e.Resize = "resize", e.ApplePayPaymentAuthorized = "applePay:onpaymentauthorized", e.PaypalCreateOrder = "paypalCreateOrder", e.PaypalOrderProcessed = "paypalOrderProcessed", e.PerformVerifyResult = "processor.message.performVerifyResult", e.ApplyCoupon = "applyCoupon", e.RequestSize = "processor.message.requestSize", e.TokenResponse = "processor.message.tokenResponse", e.Interaction = "interaction", e.LoadConfirmationRequest = "processor.message.loadConfirmationRequest", e;
    }(bP || {}),
    wP = _g;
  Si({
    target: "Array",
    stat: !0,
    forced: !_c(function (e) {
      Array.from(e);
    })
  }, {
    from: wP
  });
  var kP = ut,
    PP = hl;
  Si({
    target: "Object",
    stat: !0,
    forced: A(function () {
      PP(1);
    })
  }, {
    keys: function (e) {
      return PP(kP(e));
    }
  });
  var xP = Tr,
    SP = Kf,
    CP = ae,
    EP = RangeError,
    TP = function (e) {
      var t = SP(CP(this)),
        n = "",
        r = xP(e);
      if (r < 0 || r === 1 / 0) throw new EP("Wrong number of repetitions");
      for (; r > 0; (r >>>= 1) && (t += t)) 1 & r && (n += t);
      return n;
    },
    OP = W,
    IP = Br,
    AP = Kf,
    LP = ae,
    jP = OP(TP),
    RP = OP("".slice),
    BP = Math.ceil,
    _P = function (e) {
      return function (t, n, r) {
        var i,
          o,
          a = AP(LP(t)),
          s = IP(n),
          u = a.length,
          c = void 0 === r ? " " : AP(r);
        return s <= u || "" === c ? a : ((o = jP(c, BP((i = s - u) / c.length))).length > i && (o = RP(o, 0, i)), e ? a + o : o + a);
      };
    },
    NP = {
      start: _P(!1),
      end: _P(!0)
    },
    FP = /Version\/10(?:\.\d+){1,2}(?: [\w./]+)?(?: Mobile\/\w+)? Safari\//.test(me),
    MP = NP.start;
  Si({
    target: "String",
    proto: !0,
    forced: FP
  }, {
    padStart: function (e) {
      return MP(this, e, arguments.length > 1 ? arguments[1] : void 0);
    }
  }), Si({
    target: "String",
    proto: !0
  }, {
    repeat: TP
  });
  var UP = function () {
      return d(function e(t) {
        var n, r;
        f(this, e), this.cb = null, this.cb = null, this.listeners = [], this.onSend = null == t ? void 0 : t.onSend, this.eventName = null !== (n = null == t ? void 0 : t.eventName) && void 0 !== n ? n : "processor.payment.form.private", this.key = null !== (r = null == t ? void 0 : t.key) && void 0 !== r ? r : "processor.payment.form.private.key", this.startListening();
      }, [{
        key: "destroy",
        value: function () {
          this.cb && (window.removeEventListener("message", this.cb), this.cb = null), this.listeners = [];
        }
      }, {
        key: "sendPublicMessage",
        value: function (e, t) {
          this.sendMessage(e, t);
        }
      }, {
        key: "sendPrivateMessage",
        value: function (e, t) {
          this.sendMessage({
            type: this.eventName,
            payload: this.encryptXor(this.key, JSON.stringify(e))
          }, t);
        }
      }, {
        key: "subscribeForPrivate",
        value: function (e) {
          this.subscribe(e);
        }
      }, {
        key: "subscribeForPublic",
        value: function (e) {
          this.subscribe(e);
        }
      }, {
        key: "unsubscribe",
        value: function (e) {
          this.listeners = this.listeners.filter(function (t) {
            return t !== e;
          });
        }
      }, {
        key: "encrypt",
        value: function (e) {
          return this.encryptXor(this.key, e);
        }
      }, {
        key: "decrypt",
        value: function (e) {
          return this.decryptXor(this.key, e);
        }
      }, {
        key: "sendMessage",
        value: function (e, t) {
          t ? t.postMessage(e, "*") : window.parent ? window.parent.postMessage(e, "*") : window.top ? window.top.postMessage(e, "*") : window.postMessage(e, "*"), this.onSend && this.onSend(e);
        }
      }, {
        key: "subscribe",
        value: function (e) {
          this.listeners.push(e);
        }
      }, {
        key: "startListening",
        value: function () {
          var e = this;
          this.cb = function (t) {
            if (t.data.type) {
              var n = t;
              t.data.type === e.eventName && (n = JSON.parse(e.decryptXor(e.key, t.data.payload))), e.listeners.forEach(function (e) {
                return e(n);
              });
            }
          }, window.addEventListener("message", this.cb);
        }
      }, {
        key: "decryptXor",
        value: function (e, t) {
          try {
            for (var n = (t.match(/.{1,2}/g) || []).map(function (e) {
                return parseInt(e, 16);
              }), r = [], i = 0; i < n.length; i++) r.push(this.padStart((n[i] ^ e.charCodeAt(Math.floor(i % e.length))).toString(16), 2, "0"));
            return decodeURIComponent("%" + (r.join("").match(/.{1,2}/g) || []).join("%"));
          } catch (o) {
            return "";
          }
        }
      }, {
        key: "encryptXor",
        value: function (e, t) {
          for (var n = this, r = [], i = (Array.from(t).map(function (e) {
              return e.charCodeAt(0) < 128 ? n.padStart(e.charCodeAt(0).toString(16), 2, "0") : encodeURIComponent(e).replace(/%/g, "").toLowerCase();
            }).join("").match(/.{1,2}/g) || []).map(function (e) {
              return parseInt(e, 16);
            }), o = 0; o < i.length; o++) r.push(i[o] ^ e.charCodeAt(Math.floor(o % e.length)));
          return (r = r.map(function (e) {
            return n.padStart(e.toString(16), 2, "0");
          })).join("");
        }
      }, {
        key: "padStart",
        value: function (e, t, n) {
          return t |= 0, n = String(n || " "), e.length > t ? e : ((t -= e.length) > n.length && (n += n.repeat(t / n.length)), n.slice(0, t) + String(e));
        }
      }]);
    }(),
    DP = function (e) {
      return e.Success = "success", e.Fail = "fail", e.Redirect = "formRedirect", e.Verify = "verify", e.StartCheckStatus = "startCheckStatus", e.Card = "card", e.CustomStylesAppended = "customStylesAppended", e.PaymentButtonsInit = "_paymentButtonsInit", e.FormReady = "processor.private.event.formReady", e.PrivateResize = "_resize", e.AppleCompletePayment = "_appleCompletePayment", e.Tracking = "processor.private.event.tracking", e.PerformVerifyFlow = "processor.private.performVerifyFlow", e.UpdateComplete = "processor.private.updateComplete", e.StatusPageShown = "processor.private.statusPageShown", e.ModalStatusShown = "processor.private.modalStatusShown", e.TokenRequest = "processor.private.tokenRequest", e.OrderStatus = "orderStatus", e.CouponApplied = "couponApplied", e.FormLoadingError = "__provider_form_loading_error__", e.PrivateInteraction = "processor.private.interaction", e.PaypalOrderToken = "paypalOrderToken", e.LoadConfirmationResponse = "processor.private.loadConfirmationResponse", e;
    }(DP || {}),
    zP = function (e) {
      return e.Submit = "submit", e.Error = "error", e;
    }(zP || {}),
    VP = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, [e])).name = "EventListenersError", r;
      }
      return g(n, e), d(n);
    }(m(Error)),
    qP = function () {
      return d(function e(t) {
        f(this, e), this.logger = t, this.listeners = {}, this.allowedEventNames = [bP.Mounted, zP.Error, zP.Submit, DP.Success, DP.Fail, DP.StartCheckStatus, DP.AppleCompletePayment, DP.PaymentButtonsInit, DP.PrivateResize, bP.Resize, DP.OrderStatus, DP.Redirect, DP.Card, DP.Verify, bP.Interaction, DP.CustomStylesAppended], this.suspendedEventNames = [DP.StartCheckStatus, DP.AppleCompletePayment, DP.PaymentButtonsInit, DP.PrivateResize];
      }, [{
        key: "on",
        value: function (e, t) {
          if (this.isValidSubscriberArguments(e, t)) {
            var n = function (n) {
              n.data.type === e && t(n);
            };
            this.unsubscribe(e), this.listeners[e] = n, window.addEventListener("message", n);
          }
        }
      }, {
        key: "unsubscribe",
        value: function (e) {
          this.isValidEventName(e) && (window.removeEventListener("message", this.listeners[e]), delete this.listeners[e]);
        }
      }, {
        key: "unsubscribeAll",
        value: function () {
          var e = this;
          Object.keys(this.listeners).forEach(function (t) {
            window.removeEventListener("message", e.listeners[t]), delete e.listeners[t];
          });
        }
      }, {
        key: "isValidEventName",
        value: function (e) {
          return this.allowedEventNames.includes(e) || this.logger.error(new VP("Event ".concat(e, " does not exist"))), this.suspendedEventNames.includes(e) && this.logger.warning(new VP("Event ".concat(e, " designed for private use only and might be changed any time. Please, dont rely on it."))), !0;
        }
      }, {
        key: "isValidSubscriberArguments",
        value: function (e, t) {
          return "function" != typeof t ? (this.logger.error(new VP("Subscriber for event ".concat(e, " is not a function"))), !1) : this.isValidEventName(e);
        }
      }]);
    }(),
    $P = kg;
  Si({
    target: "Object",
    stat: !0,
    arity: 2,
    forced: Object.assign !== $P
  }, {
    assign: $P
  });
  var GP = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, [e])).name = "IframeError", r;
      }
      return g(n, e), d(n, [{
        key: "is",
        value: function (e) {
          return e instanceof n;
        }
      }], [{
        key: "DoesNotExist",
        value: function (e) {
          return new n("Container for payment form with id: ".concat(e, " does not exist"));
        }
      }]);
    }(m(Error)),
    HP = function () {
      return d(function e(t) {
        var n = this;
        f(this, e), this.iframe = t, this.resolveResult = null, this.isResolved = !1, this.result = new Promise(function (e) {
          return n.resolveResult = e;
        }).then(function () {
          n.isResolved = !0;
        }), this.intervalId = setInterval(function () {
          t.isPresentInDOM() || (n.resolveResult(), clearInterval(n.intervalId));
        }, 50);
      }, [{
        key: "destroy",
        value: function () {
          clearInterval(this.intervalId), this.resolveResult();
        }
      }]);
    }(),
    WP = function () {
      function e(t, n, r, i, o) {
        var a = this;
        f(this, e), this.id = t, this.url = n, this.defaultContainerId = r, this.merchantLogger = i, this.messageBus = o, this.state = "Initial", this.isHidden = !0, this.containerId = this.defaultContainerId, this.integrityToken = "", this.unmountObservers = [], this.loadCallbacks = [], this.loadErrorCallbacks = [], this.loadErrorValue = "", this.element = document.createElement("iframe"), this.element.id = this.id, this.element.name = this.id, this.element.allow = "payment", Object.assign(this.element.style, this.applyVisibility({
          transition: "none",
          opacity: "0",
          position: "absolute"
        })), this.element.setAttribute("src", n), this.element.onload = function () {
          a.state = "Loaded", a.runLoadedProbe();
        }, this.state = "Created";
      }
      return d(e, [{
        key: "mount",
        value: function (e) {
          var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : this.defaultContainerId,
            n = arguments.length > 2 ? arguments[2] : void 0,
            r = document.getElementById(t);
          if (!r) return this.merchantLogger.error(GP.DoesNotExist(t)), void (this.state = "NoElement");
          r.appendChild(this.element), this.containerId = t, this.element.dataset.integrityToken = e, this.integrityToken = e, this.defaultWidth = n, this.state = "Mounted";
        }
      }, {
        key: "width",
        get: function () {
          var e;
          return (null === (e = this.element) || void 0 === e ? void 0 : e.width) || "";
        }
      }, {
        key: "height",
        get: function () {
          var e;
          return (null === (e = this.element) || void 0 === e ? void 0 : e.height) || "";
        }
      }, {
        key: "setIntentMetadata",
        value: function (e, t, n) {
          this.element.dataset.intentId = e, this.element.dataset.intentHost = t, this.element.dataset.paymentType = n;
        }
      }, {
        key: "resize",
        value: function (e) {
          var t = e.height,
            n = e.width;
          this.element && (this.element.height = "".concat(t, "px"), this.element.width = this.defaultWidth ? this.defaultWidth : "".concat(n, "px"));
        }
      }, {
        key: "isPresentInDOM",
        value: function () {
          if ("Destroyed" === this.state) return !1;
          var e = !1;
          if (this.element) try {
            var t = document.getElementById(this.element.id) || null;
            t && (e = t.dataset.integrityToken === this.integrityToken);
          } catch (n) {}
          return e || (this.state = "Destroyed"), e;
        }
      }, {
        key: "enableTransitions",
        value: function () {
          this.element && Object.assign(this.element.style, this.applyVisibility({
            transition: "all 100ms"
          }));
        }
      }, {
        key: "show",
        value: function () {
          this.isHidden = !1, this.element && (Object.assign(this.element.style, this.applyVisibility({
            opacity: "1",
            position: "relative"
          })), this.element.style.height = "", this.element.getBoundingClientRect());
        }
      }, {
        key: "getWindow",
        value: function () {
          return window.frames[this.id];
        }
      }, {
        key: "onLoad",
        value: function (e) {
          this.element && ("LoadConfirmed" === this.state ? e() : this.loadCallbacks.push(e));
        }
      }, {
        key: "onError",
        value: function (e) {
          this.element && ("LoadFailed" === this.state ? e(this.loadErrorValue) : this.loadErrorCallbacks.push(e));
        }
      }, {
        key: "destroy",
        value: function () {
          var e;
          this.state = "Destroyed", this.element.src = "about:blank", this.unmountObservers.forEach(function (e) {
            return e.destroy();
          }), null === (e = this.element) || void 0 === e || e.remove();
        }
      }, {
        key: "unmounted",
        value: function () {
          var e = new HP(this);
          return this.unmountObservers.push(e), e.result;
        }
      }, {
        key: "handleLoadConfirmed",
        value: function () {
          this.state = "LoadConfirmed", this.loadCallbacks.forEach(function (e) {
            return e();
          });
        }
      }, {
        key: "handleLoadFailed",
        value: function (e) {
          "Destroyed" !== this.state && (this.loadErrorValue = e, this.state = "LoadFailed", this.loadErrorCallbacks.forEach(function (t) {
            return t(e);
          }));
        }
      }, {
        key: "applyVisibility",
        value: function (e) {
          return this.isHidden ? a(a({}, e), {}, {
            height: "0px"
          }) : e;
        }
      }, {
        key: "runLoadedProbe",
        value: function () {
          var t = this,
            n = null,
            r = null,
            i = e.getLoadConfirmationRequestSchedule(),
            o = function e(i) {
              if (i.data && i.data.type === DP.LoadConfirmationResponse) return i.data.integrity === t.integrityToken ? (t.handleLoadConfirmed(), t.messageBus.unsubscribe(e), n && clearTimeout(n), void (r && clearTimeout(r))) : void 0;
            };
          n = setTimeout(function () {
            t.handleLoadFailed("Load confirmation timeout"), t.messageBus.unsubscribe(o), r && clearTimeout(r);
          }, e.LoadConfirmationTimeout), this.messageBus.subscribeForPublic(o);
          !function e() {
            var n = i.shift();
            void 0 !== n && (r = setTimeout(function () {
              t.messageBus.sendPublicMessage({
                type: bP.LoadConfirmationRequest,
                integrity: t.integrityToken
              }, t.getWindow()), e();
            }, n));
          }();
        }
      }], [{
        key: "getLoadConfirmationRequestSchedule",
        value: function () {
          for (var t = [], n = 0, r = 0; n < e.LoadConfirmationTimeout;) {
            var i = 0;
            i = r < 10 ? 10 : r < 20 ? 20 : 100, t.push(i), n += i, r += 1;
          }
          return t;
        }
      }]);
    }();
  WP.LoadConfirmationTimeout = 5e3;
  var JP = new WeakMap(),
    ZP = function () {
      return d(function e(t, n, i) {
        f(this, e), S(this, JP, void 0), this.merchantLogger = n, this.messageBus = i, r(JP, this, t), this.preloadIframe(), this.pendingIframe = this.makePendingIframe();
      }, [{
        key: "getIframe",
        value: function () {
          var e = this.pendingIframe;
          return this.pendingIframe = this.makePendingIframe(), e;
        }
      }, {
        key: "makePendingIframe",
        value: function () {
          return new WP(n(JP, this).getIframeId(), n(JP, this).getIframeUrl(), n(JP, this).getDefaultFormId(), this.merchantLogger, this.messageBus);
        }
      }, {
        key: "preloadIframe",
        value: function () {
          var e = document.createElement("link");
          e.rel = "preload", e.as = "document", e.href = n(JP, this).getIframeUrl();
        }
      }]);
    }(),
    XP = function () {
      return d(function e() {
        f(this, e);
      }, [{
        key: "getSdkReferrer",
        value: function () {
          return document.referrer;
        }
      }, {
        key: "getPageUrl",
        value: function () {
          var e;
          try {
            e = window.self !== window.top;
          } catch (t) {
            e = !0;
          }
          return e ? this.getPageUrlForIframe() : this.getPageUrlForUsualPage();
        }
      }, {
        key: "getPageUrlForIframe",
        value: function () {
          return document.referrer || this.getPageUrlForUsualPage();
        }
      }, {
        key: "getPageUrlForUsualPage",
        value: function () {
          return window.location.href;
        }
      }]);
    }();
  function YP(e, t) {
    return Object.keys(e).some(function (n) {
      return e[n] === t;
    });
  }
  var KP = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, [e])).name = "FormLoadingError", r;
      }
      return g(n, e), d(n);
    }(m(Error)),
    QP = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, [e])).name = "SdkError", r;
      }
      return g(n, e), d(n);
    }(m(Error)),
    ex = lk.values;
  Si({
    target: "Object",
    stat: !0
  }, {
    values: function (e) {
      return ex(e);
    }
  });
  var tx = function (e) {
      return e.FormSubmit = "form_v2_submitted", e;
    }(tx || {}),
    nx = function (e) {
      return e.Loading = "form_loading", e.Filling = "form_filling", e.Submit = "form_submit", e.Form3d = "form_3D", e.FormDSRP = "form_dsrp", e.Errors = "form_errors", e.After = "form_after", e;
    }(nx || {}),
    rx = function (e) {
      return e.Events = "form_events", e;
    }(rx || {}),
    ix = function () {
      function e(t, n) {
        var r = this;
        f(this, e), this.api = t, this.scriptSource = n, this.lastFormShownTime = 0, this.lastGooglePayShowTime = 0, this.lastApplePayShownTime = 0, this.formEventCustomization = p({}, tx.FormSubmit, function (e) {
          return a(a({}, e), {}, {
            value: "".concat(r.lastFormShownTime ? Date.now() - r.lastFormShownTime : 0)
          });
        });
      }
      return d(e, [{
        key: "getScriptLoadTime",
        value: function () {
          var e = this,
            t = this.getPerformance();
          if (!t || !t.getEntriesByType) return 0;
          var n = t.getEntriesByType("resource").find(function (t) {
            return t.name === e.scriptSource;
          });
          return (null == n ? void 0 : n.duration) || null;
        }
      }, {
        key: "getPerformance",
        value: function () {
          return window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || null;
        }
      }, {
        key: "getPerformanceNow",
        value: function () {
          var e = this.getPerformance();
          try {
            return e ? e.now() : 0;
          } catch (t) {
            return 0;
          }
        }
      }, {
        key: "fromForm",
        value: function (e) {
          var t = a({}, e);
          delete t.type, Object.values(tx).includes(t.event) ? this.api.send(this.formEventCustomization[t.event](t)) : this.api.send(t);
        }
      }, {
        key: "init",
        value: function (t, n) {
          this.api.init(t, n, e.entityName);
        }
      }, {
        key: "clear",
        value: function () {
          this.api.clear();
        }
      }, {
        key: "scriptLoadTime",
        value: function () {
          var e = this.getScriptLoadTime();
          null !== e && this.api.send({
            event: "form_v2_script_load_time",
            category: rx.Events,
            level: nx.Loading,
            value: e.toString(10)
          });
        }
      }, {
        key: "initNetworkError",
        value: function (e) {
          e > 0 && this.api.send({
            event: "form_v2_init_network_error",
            category: rx.Events,
            level: nx.Loading,
            value: e.toString(10)
          });
        }
      }, {
        key: "resignInitTime",
        value: function () {
          var e = this,
            t = this.getPerformanceNow();
          return t ? function () {
            e.lastFormShownTime = Date.now();
            var n = e.getPerformanceNow();
            e.api.send({
              event: "form_v2_resign_init_time",
              category: rx.Events,
              level: nx.Loading,
              value: (t - n).toString(10)
            });
          } : function () {};
        }
      }, {
        key: "initTime",
        value: function () {
          var e = this,
            t = this.getPerformanceNow();
          if (!t) return {
            formLoadEnded: function () {},
            buttonsLoadEnded: function () {}
          };
          var n = t,
            r = t,
            i = !1,
            o = !1,
            a = !1,
            s = function () {
              a && !i || !o || e.api.send({
                event: "form_v2_init_time",
                category: rx.Events,
                level: nx.Loading,
                value: a ? (n - t).toString(10) : "0",
                context: (r - t).toString(10)
              });
            };
          return {
            buttonsLoadEnded: function (t) {
              n = e.getPerformanceNow(), i = !0, a = t, s();
            },
            formLoadEnded: function (t) {
              e.lastFormShownTime = Date.now(), r = e.getPerformanceNow(), o = !0, a = t, s();
            }
          };
        }
      }, {
        key: "updateTime",
        value: function () {
          var e = this,
            t = this.getPerformanceNow();
          return t ? function () {
            e.api.send({
              event: "form_v2_update_init",
              category: rx.Events,
              level: nx.Loading,
              value: (e.getPerformanceNow() - t).toString(10)
            });
          } : function () {};
        }
      }, {
        key: "appleButtonMounted",
        value: function () {
          this.lastApplePayShownTime = Date.now(), this.api.send({
            event: "applebtn_mounted",
            category: rx.Events,
            level: nx.Loading
          });
        }
      }, {
        key: "appleButtonPageOpened",
        value: function () {
          this.api.send({
            event: "applepaybtn_opened",
            category: rx.Events,
            level: nx.FormDSRP
          });
        }
      }, {
        key: "appleButtonPageClosed",
        value: function () {
          this.api.send({
            event: "applepaybtn_closed",
            category: rx.Events,
            level: nx.FormDSRP
          });
        }
      }, {
        key: "appleButtonSubmitted",
        value: function () {
          this.api.send({
            event: "applepay_submitted",
            category: rx.Events,
            level: nx.Submit,
            value: "".concat(this.lastApplePayShownTime ? Date.now() - this.lastApplePayShownTime : 0)
          });
        }
      }, {
        key: "googleButtonMounted",
        value: function () {
          this.lastGooglePayShowTime = Date.now(), this.api.send({
            event: "googlebtn_mounted",
            category: rx.Events,
            level: nx.Loading
          });
        }
      }, {
        key: "googleButtonPageOpened",
        value: function () {
          this.api.send({
            event: "googlebtn_page_opened",
            category: rx.Events,
            level: nx.FormDSRP
          });
        }
      }, {
        key: "googleButtonPageClosed",
        value: function () {
          this.api.send({
            event: "googlebtn_page_closed",
            category: rx.Events,
            level: nx.FormDSRP
          });
        }
      }, {
        key: "googleButtonPageSubmitted",
        value: function () {
          this.api.send({
            event: "googlebtn_page_submitted",
            category: rx.Events,
            level: nx.Submit,
            value: "".concat(this.lastGooglePayShowTime ? Date.now() - this.lastGooglePayShowTime : 0)
          });
        }
      }, {
        key: "paypalButtonMountTime",
        value: function () {
          var e = this,
            t = this.getPerformanceNow();
          return t ? function () {
            e.api.send({
              event: "paypalbtn_mounted",
              category: rx.Events,
              level: nx.Loading,
              value: (e.getPerformanceNow() - t).toString(10)
            });
          } : function () {};
        }
      }, {
        key: "updateIntentStarted",
        value: function () {
          this.api.send({
            event: "form_v2_intent_update",
            level: nx.Loading,
            category: rx.Events
          });
        }
      }, {
        key: "domainsUsage",
        value: function (e) {
          this.api.send({
            event: "request_v2_from_domain",
            level: nx.Loading,
            category: rx.Events,
            context: e.sdkReferrer,
            value: this.getDomainName(e.pageUrl)
          }), this.api.send({
            event: "request_v2_from_url",
            level: nx.Loading,
            context: e.sdkReferrer,
            category: rx.Events,
            value: e.pageUrl
          });
        }
      }, {
        key: "legacyBrowsersTest",
        value: function () {
          this.api.send({
            event: "form_v2_legacy_browsers_test",
            level: nx.Loading,
            category: rx.Events
          });
        }
      }, {
        key: "getDomainName",
        value: function (e) {
          if (e) {
            var t = new URL(e).hostname.split(".").reverse();
            return t.length >= 3 && t[1].match(/^(com|edu|gov|net|mil|org|nom|co|name|info|biz)$/i) ? "".concat(t[2], ".").concat(t[1], ".").concat(t[0]) : "".concat(t[1], ".").concat(t[0]);
          }
          return "";
        }
      }]);
    }();
  ix.entityName = "track_id";
  var ox = function () {
      function e(t, n, r, i) {
        var o = this;
        f(this, e), this.context = t, this.tracking = n, this.logger = r, this.messageBus = i, this.messageBus.subscribeForPublic(function (e) {
          return o.withLogger(function () {
            return o.processPublicMessage(e);
          });
        }), this.messageBus.subscribeForPrivate(function (e) {
          return o.withLogger(function () {
            return o.processMessage(e, !0);
          });
        });
      }
      return d(e, [{
        key: "withLogger",
        value: function (e) {
          try {
            e();
          } catch (UO) {
            UO instanceof Error && this.logger.error(new QP(UO.toString()), UO);
          }
        }
      }, {
        key: "processPublicMessage",
        value: function (t) {
          t.data && t.data.type && (YP(DP, t.data.type) || YP(bP, t.data.type) || YP(zP, t.data.type)) && this.processMessage(t.data, e.isCrossOriginMessage(t));
        }
      }, {
        key: "processMessage",
        value: function (e, t) {
          switch (e.type) {
            case DP.Fail:
              this.handleFail();
              break;
            case DP.Success:
              this.handleSuccess();
              break;
            case DP.PrivateResize:
              this.handlePrivateResize(e, t);
              break;
            case DP.Redirect:
              this.handleRedirect();
              break;
            case DP.StartCheckStatus:
              this.handleStartCheckStatus(e);
              break;
            case DP.AppleCompletePayment:
              this.handleAppleCompletePayment(e);
              break;
            case DP.FormLoadingError:
              this.handleFormLoadingError(e);
              break;
            case DP.PrivateInteraction:
              this.handleInteraction(e);
              break;
            case DP.ModalStatusShown:
              this.handleModalStatusShown();
              break;
            case DP.StatusPageShown:
              this.handleStatusPageShown();
              break;
            case DP.PerformVerifyFlow:
              this.handlePerformVerifyFlow(e);
              break;
            case DP.TokenRequest:
              this.handleTokenRequest(e);
              break;
            case DP.Tracking:
              this.handleTracking(e);
          }
        }
      }, {
        key: "handleFail",
        value: function () {
          var e;
          null === (e = this.context.threeDSFlow) || void 0 === e || e.close();
        }
      }, {
        key: "handleSuccess",
        value: function () {
          var e;
          null === (e = this.context.threeDSFlow) || void 0 === e || e.close();
        }
      }, {
        key: "handlePrivateResize",
        value: function (e, t) {
          if (t) {
            var n = this.context.resize(e),
              r = n.width,
              i = n.height;
            n.visible && this.messageBus.sendPublicMessage({
              type: bP.Resize,
              width: r,
              height: i
            });
          }
        }
      }, {
        key: "handleRedirect",
        value: function () {
          var e, t;
          null === (e = this.context.paymentsButtons) || void 0 === e || e.destroy(), null === (t = this.context.iframe) || void 0 === t || t.show();
        }
      }, {
        key: "handleStartCheckStatus",
        value: function (e) {
          var t;
          null === (t = this.context.paymentsButtons) || void 0 === t || t.setIsDisabled(e.value);
        }
      }, {
        key: "handleAppleCompletePayment",
        value: function (e) {
          var t;
          null === (t = this.context.paymentsButtons) || void 0 === t || t.completeApplePayment(e.success);
        }
      }, {
        key: "handleFormLoadingError",
        value: function (e) {
          this.logger.error(new KP(e.message));
        }
      }, {
        key: "handleInteraction",
        value: function (e) {
          var t;
          null === (t = this.context.interactionsNotifier) || void 0 === t || t.processFormMessage(e);
        }
      }, {
        key: "handleModalStatusShown",
        value: function () {
          var e;
          null === (e = this.context.threeDSFlow) || void 0 === e || e.close();
        }
      }, {
        key: "handleStatusPageShown",
        value: function () {
          var e, t;
          null === (e = this.context.paymentsButtons) || void 0 === e || e.destroy(), null === (t = this.context.iframe) || void 0 === t || t.show();
        }
      }, {
        key: "handlePerformVerifyFlow",
        value: function (e) {
          this.context.choose3DSFlowScenario(e.verifyType, e.url, e.message);
        }
      }, {
        key: "handleTokenRequest",
        value: function (e) {
          this.context.sendTokenToForm(e.intentId);
        }
      }, {
        key: "handleTracking",
        value: function (e) {
          var t = this.context.getLastKnownIntentTracking();
          this.tracking.fromForm(a(a({}, e), {}, {
            entityName: ix.entityName,
            entityValue: null == t ? void 0 : t.trackId,
            signature: null == t ? void 0 : t.trackSignature
          }));
        }
      }], [{
        key: "isCrossOriginMessage",
        value: function (e) {
          return !!window.location.origin && e.origin !== window.location.origin;
        }
      }]);
    }(),
    ax = function (e) {
      return e.Default = "default", e.Modal = "modal", e.Tab = "tab", e;
    }(ax || {}),
    sx = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, ["Unable to init payment: ".concat(JSON.stringify(e))])).name = "InitPaymentError", r.details = e, r;
      }
      return g(n, e), d(n);
    }(m(Error)),
    ux = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, [e])).name = "SdkTokenError", r;
      }
      return g(n, e), d(n);
    }(m(Error)),
    cx = Kt.f,
    lx = L,
    fx = O,
    hx = W,
    dx = vi,
    px = Ad,
    gx = mn,
    vx = Rl,
    yx = xr.f,
    mx = ye,
    bx = kh,
    wx = Kf,
    kx = ah,
    Px = fb,
    xx = function (e, t, n) {
      n in e || cx(e, n, {
        configurable: !0,
        get: function () {
          return t[n];
        },
        set: function (e) {
          t[n] = e;
        }
      });
    },
    Sx = Pr,
    Cx = A,
    Ex = ft,
    Tx = Qn.enforce,
    Ox = ta,
    Ix = pb,
    Ax = yb,
    Lx = Ct("match"),
    jx = fx.RegExp,
    Rx = jx.prototype,
    Bx = fx.SyntaxError,
    _x = hx(Rx.exec),
    Nx = hx("".charAt),
    Fx = hx("".replace),
    Mx = hx("".indexOf),
    Ux = hx("".slice),
    Dx = /^\?<[^\s\d!#%&*+<=>@^][^\s!#%&*+<=>@^]*>/,
    zx = /a/g,
    Vx = /a/g,
    qx = new jx(zx) !== zx,
    $x = Px.MISSED_STICKY,
    Gx = Px.UNSUPPORTED_Y,
    Hx = lx && (!qx || $x || Ix || Ax || Cx(function () {
      return Vx[Lx] = !1, jx(zx) !== zx || jx(Vx) === Vx || "/a/i" !== String(jx(zx, "i"));
    }));
  if (dx("RegExp", Hx)) {
    for (var Wx = function (e, t) {
        var n,
          r,
          i,
          o,
          a,
          s,
          u = mx(Rx, this),
          c = bx(e),
          l = void 0 === t,
          f = [],
          h = e;
        if (!u && c && l && e.constructor === Wx) return e;
        if ((c || mx(Rx, e)) && (e = e.source, l && (t = kx(h))), e = void 0 === e ? "" : wx(e), t = void 0 === t ? "" : wx(t), h = e, Ix && ("dotAll" in zx) && (r = !!t && Mx(t, "s") > -1) && (t = Fx(t, /s/g, "")), n = t, $x && ("sticky" in zx) && (i = !!t && Mx(t, "y") > -1) && Gx && (t = Fx(t, /y/g, "")), Ax && (o = function (e) {
          for (var t, n = e.length, r = 0, i = "", o = [], a = vx(null), s = !1, u = !1, c = 0, l = ""; r <= n; r++) {
            if ("\\" === (t = Nx(e, r))) t += Nx(e, ++r);else if ("]" === t) s = !1;else if (!s) switch (!0) {
              case "[" === t:
                s = !0;
                break;
              case "(" === t:
                _x(Dx, Ux(e, r + 1)) && (r += 2, u = !0), i += t, c++;
                continue;
              case ">" === t && u:
                if ("" === l || Ex(a, l)) throw new Bx("Invalid capture group name");
                a[l] = !0, o[o.length] = [l, c], u = !1, l = "";
                continue;
            }
            u ? l += t : i += t;
          }
          return [i, o];
        }(e), e = o[0], f = o[1]), a = px(jx(e, t), u ? this : Rx, Wx), (r || i || f.length) && (s = Tx(a), r && (s.dotAll = !0, s.raw = Wx(function (e) {
          for (var t, n = e.length, r = 0, i = "", o = !1; r <= n; r++) "\\" !== (t = Nx(e, r)) ? o || "." !== t ? ("[" === t ? o = !0 : "]" === t && (o = !1), i += t) : i += "[\\s\\S]" : i += t + Nx(e, ++r);
          return i;
        }(e), n)), i && (s.sticky = !0), f.length && (s.groups = f)), e !== h) try {
          gx(a, "source", "" === h ? "(?:)" : h);
        } catch (UO) {}
        return a;
      }, Jx = yx(jx), Zx = 0; Jx.length > Zx;) xx(Wx, jx, Jx[Zx++]);
    Rx.constructor = Wx, Wx.prototype = Rx, Sx(fx, "RegExp", Wx, {
      constructor: !0
    });
  }
  Ox("RegExp");
  var Xx = "\t\n\v\f\r                　\u2028\u2029\ufeff",
    Yx = ae,
    Kx = Kf,
    Qx = Xx,
    eS = W("".replace),
    tS = RegExp("^[" + Qx + "]+"),
    nS = RegExp("(^|[^" + Qx + "])[" + Qx + "]+$"),
    rS = function (e) {
      return function (t) {
        var n = Kx(Yx(t));
        return 1 & e && (n = eS(n, tS, "")), 2 & e && (n = eS(n, nS, "$1")), n;
      };
    },
    iS = {
      start: rS(1),
      end: rS(2),
      trim: rS(3)
    },
    oS = Cn.PROPER,
    aS = A,
    sS = Xx,
    uS = function (e) {
      return aS(function () {
        return !!sS[e]() || "​᠎" !== "​᠎"[e]() || oS && sS[e].name !== e;
      });
    },
    cS = iS.trim;
  Si({
    target: "String",
    proto: !0,
    forced: uS("trim")
  }, {
    trim: function () {
      return cS(this);
    }
  });
  var lS = {
    type: "tel",
    maxLength: 14,
    mask: function (e) {
      return e.replace(/[^\d]/g, "").replace(/(.{3})/, "$1.").replace(/(.{7})/, "$1.").replace(/(.{11})/, "$1-").replace(/\.$|-$/, "");
    },
    regexp: "[0-9]{11,14}",
    validator: function (e) {
      var t,
        n = e.replace(/[^\d]+/g, ""),
        r = 1;
      if (11 !== n.length) return !1;
      for (t = 0; t < n.length - 1; t++) if (n.charAt(t) !== n.charAt(t + 1)) {
        r = 0;
        break;
      }
      if (1 === r) return !1;
      var i = n.substring(0, 9),
        o = n.substring(9),
        a = 0;
      for (t = 10; t > 1; t--) a += parseInt(i.charAt(10 - t)) * t;
      var s = a % 11 < 2 ? 0 : 11 - a % 11;
      if (s.toString() !== o.charAt(0)) return !1;
      for (i = n.substring(0, 10), a = 0, t = 11; t > 1; t--) a += parseInt(i.charAt(11 - t)) * t;
      return (s = a % 11 < 2 ? 0 : 11 - a % 11).toString() === o.charAt(1);
    }
  };
  var fS = function (e) {
    return function () {
      return e;
    };
  };
  var hS = function (e) {
    return function (t, n, r) {
      for (var i = -1, o = Object(t), a = r(t), s = a.length; s--;) {
        var u = a[e ? s : ++i];
        if (!1 === n(o[u], u, o)) break;
      }
      return t;
    };
  }();
  var dS = function (e, t) {
      for (var n = -1, r = Array(e); ++n < e;) r[n] = t(n);
      return r;
    },
    pS = "object" == typeof C && C && C.Object === Object && C,
    gS = pS,
    vS = "object" == typeof self && self && self.Object === Object && self,
    yS = gS || vS || Function("return this")(),
    mS = yS.Symbol,
    bS = mS,
    wS = Object.prototype,
    kS = wS.hasOwnProperty,
    PS = wS.toString,
    xS = bS ? bS.toStringTag : void 0;
  var SS = function (e) {
      var t = kS.call(e, xS),
        n = e[xS];
      try {
        e[xS] = void 0;
        var r = !0;
      } catch (o) {}
      var i = PS.call(e);
      return r && (t ? e[xS] = n : delete e[xS]), i;
    },
    CS = Object.prototype.toString;
  var ES = SS,
    TS = function (e) {
      return CS.call(e);
    },
    OS = mS ? mS.toStringTag : void 0;
  var IS = function (e) {
    return null == e ? void 0 === e ? "[object Undefined]" : "[object Null]" : OS && OS in Object(e) ? ES(e) : TS(e);
  };
  var AS = function (e) {
      return null != e && "object" == typeof e;
    },
    LS = IS,
    jS = AS;
  var RS = function (e) {
      return jS(e) && "[object Arguments]" == LS(e);
    },
    BS = AS,
    _S = Object.prototype,
    NS = _S.hasOwnProperty,
    FS = _S.propertyIsEnumerable,
    MS = RS(function () {
      return arguments;
    }()) ? RS : function (e) {
      return BS(e) && NS.call(e, "callee") && !FS.call(e, "callee");
    },
    US = MS,
    DS = Array.isArray,
    zS = {
      exports: {}
    };
  var VS = function () {
    return !1;
  };
  !function (e, t) {
    var n = yS,
      r = VS,
      i = t && !t.nodeType && t,
      o = i && e && !e.nodeType && e,
      a = o && o.exports === i ? n.Buffer : void 0,
      s = (a ? a.isBuffer : void 0) || r;
    e.exports = s;
  }(zS, zS.exports);
  var qS = zS.exports,
    $S = /^(?:0|[1-9]\d*)$/;
  var GS = function (e, t) {
    var n = typeof e;
    return !!(t = null == t ? 9007199254740991 : t) && ("number" == n || "symbol" != n && $S.test(e)) && e > -1 && e % 1 == 0 && e < t;
  };
  var HS = function (e) {
      return "number" == typeof e && e > -1 && e % 1 == 0 && e <= 9007199254740991;
    },
    WS = IS,
    JS = HS,
    ZS = AS,
    XS = {};
  XS["[object Float32Array]"] = XS["[object Float64Array]"] = XS["[object Int8Array]"] = XS["[object Int16Array]"] = XS["[object Int32Array]"] = XS["[object Uint8Array]"] = XS["[object Uint8ClampedArray]"] = XS["[object Uint16Array]"] = XS["[object Uint32Array]"] = !0, XS["[object Arguments]"] = XS["[object Array]"] = XS["[object ArrayBuffer]"] = XS["[object Boolean]"] = XS["[object DataView]"] = XS["[object Date]"] = XS["[object Error]"] = XS["[object Function]"] = XS["[object Map]"] = XS["[object Number]"] = XS["[object Object]"] = XS["[object RegExp]"] = XS["[object Set]"] = XS["[object String]"] = XS["[object WeakMap]"] = !1;
  var YS = function (e) {
    return ZS(e) && JS(e.length) && !!XS[WS(e)];
  };
  var KS = function (e) {
      return function (t) {
        return e(t);
      };
    },
    QS = {
      exports: {}
    };
  !function (e, t) {
    var n = pS,
      r = t && !t.nodeType && t,
      i = r && e && !e.nodeType && e,
      o = i && i.exports === r && n.process,
      a = function () {
        try {
          var e = i && i.require && i.require("util").types;
          return e || o && o.binding && o.binding("util");
        } catch (t) {}
      }();
    e.exports = a;
  }(QS, QS.exports);
  var eC = QS.exports,
    tC = YS,
    nC = KS,
    rC = eC && eC.isTypedArray,
    iC = rC ? nC(rC) : tC,
    oC = dS,
    aC = US,
    sC = DS,
    uC = qS,
    cC = GS,
    lC = iC,
    fC = Object.prototype.hasOwnProperty;
  var hC = function (e, t) {
      var n = sC(e),
        r = !n && aC(e),
        i = !n && !r && uC(e),
        o = !n && !r && !i && lC(e),
        a = n || r || i || o,
        s = a ? oC(e.length, String) : [],
        u = s.length;
      for (var c in e) !t && !fC.call(e, c) || a && ("length" == c || i && ("offset" == c || "parent" == c) || o && ("buffer" == c || "byteLength" == c || "byteOffset" == c) || cC(c, u)) || s.push(c);
      return s;
    },
    dC = Object.prototype;
  var pC = function (e) {
    var t = e && e.constructor;
    return e === ("function" == typeof t && t.prototype || dC);
  };
  var gC = function (e, t) {
      return function (n) {
        return e(t(n));
      };
    }(Object.keys, Object),
    vC = pC,
    yC = gC,
    mC = Object.prototype.hasOwnProperty;
  var bC = IS,
    wC = function (e) {
      var t = typeof e;
      return null != e && ("object" == t || "function" == t);
    };
  var kC = function (e) {
      if (!wC(e)) return !1;
      var t = bC(e);
      return "[object Function]" == t || "[object GeneratorFunction]" == t || "[object AsyncFunction]" == t || "[object Proxy]" == t;
    },
    PC = HS;
  var xC = hC,
    SC = function (e) {
      if (!vC(e)) return yC(e);
      var t = [];
      for (var n in Object(e)) mC.call(e, n) && "constructor" != n && t.push(n);
      return t;
    },
    CC = function (e) {
      return null != e && PC(e.length) && !kC(e);
    };
  var EC = hS,
    TC = function (e) {
      return CC(e) ? xC(e) : SC(e);
    };
  var OC = function (e, t) {
    return e && EC(e, t, TC);
  };
  var IC = function (e, t, n, r) {
    return OC(e, function (e, i, o) {
      t(r, n(e), i, o);
    }), r;
  };
  var AC = fS,
    LC = function (e, t) {
      return function (n, r) {
        return IC(n, e, t(r), {});
      };
    },
    jC = function (e) {
      return e;
    },
    RC = Object.prototype.toString;
  var BC = E(LC(function (e, t, n) {
    null != t && "function" != typeof t.toString && (t = RC.call(t)), e[t] = n;
  }, AC(jC)));
  var _C = new function (e) {
    var t,
      n = e ? e.preset : "ru",
      r = {
        "а": "a",
        "б": "b",
        "в": "v",
        "д": "d",
        "з": "z",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "ь": ""
      };
    "ru" === n ? Object.assign(r, {
      "г": "g",
      "и": "i",
      "ъ": "",
      "ы": "i",
      "э": "e"
    }) : "uk" === n ? Object.assign(r, {
      "г": "h",
      "ґ": "g",
      "е": "e",
      "и": "y",
      "і": "i",
      "'": "",
      "’": "",
      "ʼ": ""
    }) : "mn" === n && Object.assign(r, {
      "г": "g",
      "ө": "o",
      "ү": "u",
      "и": "i",
      "ы": "y",
      "э": "e",
      "ъ": ""
    }), "ru" === n ? t = Object.assign(BC(r), {
      i: "и",
      "": ""
    }) : ("uk" === n || "mn" === n) && (t = Object.assign(BC(r), {
      "": ""
    }));
    var i,
      o = "ru" === n ? {
        "е": "ye"
      } : {
        "є": "ye",
        "ї": "yi"
      },
      a = {
        "ё": "yo",
        "ж": "zh",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ю": "yu",
        "я": "ya"
      },
      s = Object.assign({}, a, o),
      u = Object.assign(BC(s)),
      c = Object.assign(r, s),
      l = Object.assign({}, r, {
        "й": "i"
      });
    "ru" === n ? Object.assign(l, {
      "е": "e"
    }) : "uk" === n ? Object.assign(l, {
      "ї": "i"
    }) : "mn" === n && Object.assign(l, {
      "е": "e"
    }), "ru" === n ? i = Object.assign(BC(r), {
      i: "и",
      y: "ы",
      e: "е",
      "": ""
    }) : "uk" === n && (i = Object.assign(BC(r), {
      "": ""
    }));
    var f = {};
    "uk" === n && (f = {
      "є": "ie",
      "ю": "iu",
      "я": "ia"
    });
    var h = Object.assign(a, f),
      d = Object.assign(BC(h)),
      p = Object.assign(l, h);
    return {
      transform: function (e, t) {
        if (!e) return "";
        for (var r = e.normalize(), i = "", o = !1, a = 0; a < r.length; a++) {
          var s = r[a] === r[a].toUpperCase(),
            u = r[a].toLowerCase();
          if (" " !== u) {
            var l = void 0;
            "uk" === n && "зг" === r.slice(a - 1, a + 1).toLowerCase() ? l = "gh" : 0 === a || o ? (l = c[u], o = !1) : l = p[u], void 0 === l ? i += s ? u.toUpperCase() : u : s ? l.length > 1 ? i += l[0].toUpperCase() + l.slice(1) : i += l.toUpperCase() : i += l;
          } else i += t || " ", o = !0;
        }
        return i;
      },
      reverse: function (e, n) {
        if (!e) return "";
        for (var r = e.normalize(), o = "", a = !1, s = 0; s < r.length;) {
          var c = r[s] === r[s].toUpperCase(),
            l = r[s].toLowerCase(),
            f = s;
          if (" " !== l && l !== n) {
            var h = void 0,
              p = r.slice(s, s + 2).toLowerCase();
            0 === s || a ? ((h = u[p]) ? s += 2 : (h = t[l], s++), a = !1) : (h = d[p]) ? s += 2 : (h = i[l], s++), "shch" === r.slice(f, f + 4).toLowerCase() ? (h = "щ", s = f + 4) : "zgh" === r.slice(f - 1, f + 2).toLowerCase() && (h = "г", s = f + 2), void 0 === h ? o += c ? l.toUpperCase() : l : c ? h.length > 1 ? o += h[0].toUpperCase() + h.slice(1) : o += h.toUpperCase() : o += h;
          } else o += " ", a = !0, s++;
        }
        return o;
      }
    };
  }();
  var NC = {
    type: "text",
    maxLength: 50,
    mask: function (e) {
      return _C.transform(e).replace(/\s\s+/g, " ").replace(/^[^a-zA-Z]/g, "").replace(/[^a-zA-Z'\-. ]/g, "").toUpperCase();
    },
    regexp: "^\\w.{1,48}\\w$"
  };
  var FC = iS.start,
    MC = uS("trimStart") ? function () {
      return FC(this);
    } : "".trimStart;
  Si({
    target: "String",
    proto: !0,
    name: "trimStart",
    forced: "".trimLeft !== MC
  }, {
    trimLeft: MC
  });
  Si({
    target: "String",
    proto: !0,
    name: "trimStart",
    forced: "".trimStart !== MC
  }, {
    trimStart: MC
  });
  var UC,
    DC = {
      cardPin: {
        type: "tel",
        maxLength: 4,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{4}"
      },
      zip: {
        type: "tel",
        maxLength: function (e) {
          return "USA" === (null == e ? void 0 : e.country) ? 10 : 5;
        },
        mask: function (e, t) {
          return "USA" === (null == t ? void 0 : t.country) ? e.replace(/[^\d]/g, "").replace(/(.{5})/, "$1-").replace(/\.$|-$/, "") : e.replace(/[^\d]/g, "");
        },
        regexp: function (e) {
          return "USA" === (null == e ? void 0 : e.country) ? "^[0-9]{5}(?:[0-9]{4})?$" : "[0-9]{5}";
        }
      },
      cardHolder: NC,
      argentinaDni: {
        type: "tel",
        maxLength: 11,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{2})/, "$1.").replace(/(.{6})/, "$1.").replace(/\.$|-$/, "");
        },
        regexp: "[0-9]{7,9}"
      },
      bangladeshNic: {
        type: "tel",
        maxLength: 19,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{3})/, "$1 ").replace(/(.{7})/, "$1 ").trim();
        },
        regexp: "[0-9]{13,17}"
      },
      boliviaCi: {
        type: "tel",
        maxLength: 22,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{2})/, "$1.").replace(/(.{6})/, "$1.").replace(/\.$|-$/, "");
        },
        regexp: "[0-9]{5,20}"
      },
      brazilCpf: lS,
      cameroonCni: {
        type: "tel",
        maxLength: 8,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{8}"
      },
      chileCi: {
        type: "tel",
        maxLength: 10,
        mask: function (e) {
          var t = e.toUpperCase();
          return "-" === t.charAt(t.length - 1) && (t = t.slice(0, t.length - 1)), 8 !== t.length || t.includes("-") || (t = "".concat(t.slice(0, 7), "-").concat(t.slice(7, 8))), 9 !== t.length || t.includes("-") || (t = "".concat(t.slice(0, 8), "-").concat(t.slice(8, 9))), "-" === (t = t.split("").filter(function (e, t) {
            return !("-" === e && ![7, 8].includes(t));
          }).join("")).charAt(7) && "-" === t.charAt(8) && (t = "".concat(t.slice(0, 7)).concat(t.slice(8, t.length))), "-" === t.charAt(7) && 10 === t.length && (t = "".concat(t.slice(0, 7)).concat(t.charAt(8), "-").concat(t.charAt(9))), t.replace(/[^a-zA-Z0-9-]/g, "");
        },
        regexp: "[a-zA-Z0-9]{8,9}"
      },
      chinaId: {
        type: "tel",
        maxLength: 20,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{5,20}"
      },
      colombiaCc: {
        type: "tel",
        maxLength: 10,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{6,10}"
      },
      costaRicaCi: {
        type: "tel",
        maxLength: 11,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{1})/, "$1 ").replace(/(.{6})/, "$1 ").trim();
        },
        regexp: "[0-9]{9}"
      },
      dominicanaId: {
        type: "tel",
        maxLength: 13,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{3})/, "$1-").replace(/(.{11})/, "$1-").replace(/\.$|-$/, "");
        },
        regexp: "[0-9]{11}"
      },
      ecuadorCi: {
        type: "tel",
        maxLength: 22,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{4})/, "$1.").replace(/(.{7})/, "$1.").replace(/\.$|-$/, "");
        },
        regexp: "[0-9]{5,20}"
      },
      elSalvadorId: {
        type: "tel",
        maxLength: 11,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{9,11}"
      },
      egyptId: {
        type: "tel",
        maxLength: 19,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{1})/, "$1 ").replace(/(.{4})/, "$1 ").replace(/(.{7})/, "$1 ").replace(/(.{10})/, "$1 ").replace(/(.{13})/, "$1 ").trim();
        },
        regexp: "[0-9]{14}"
      },
      ghanaCard: {
        type: "tel",
        maxLength: 13,
        mask: function (e) {
          return e.replace(/[^\da-zA-Z]/g, "").toUpperCase();
        },
        regexp: "[a-zA-Z0-9]{13}"
      },
      guatemalaCui: {
        type: "tel",
        maxLength: 15,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{4})/, "$1 ").replace(/(.{10})/, "$1 ").trim();
        },
        regexp: "[0-9]{13}"
      },
      indiaPan: {
        type: "text",
        maxLength: 12,
        mask: function (e) {
          return e.replace(/[^\da-zA-Z]/g, "").replace(/(.{5})/, "$1 ").replace(/(.{10})/, "$1 ").toUpperCase().trim();
        },
        regexp: "[a-zA-Z]{5}[0-9]{4}[a-zA-Z]{1}"
      },
      indonesiaNik: {
        type: "tel",
        maxLength: 20,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{2})/, "$1 ").replace(/(.{5})/, "$1 ").replace(/(.{8})/, "$1 ").replace(/(.{15})/, "$1 ").trim();
        },
        regexp: "[0-9]{16}"
      },
      japanId: {
        type: "tel",
        maxLength: 12,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{12}"
      },
      kenyaId: {
        type: "tel",
        maxLength: 8,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{8}"
      },
      malaysiaNric: {
        type: "tel",
        maxLength: 14,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{6})/, "$1-").replace(/(.{9})/, "$1-").replace(/\.$|-$/, "");
        },
        regexp: "[0-9]{12}"
      },
      mexicoCurp: {
        type: "text",
        maxLength: 18,
        mask: function (e) {
          return e.replace(/[^\da-zA-Z]/g, "").toUpperCase();
        },
        regexp: "[a-zA-Z0-9]{10,18}"
      },
      moroccoCnie: {
        type: "text",
        maxLength: 20,
        mask: function (e) {
          return e.replace(/[^\da-zA-Z]/g, "").toUpperCase();
        },
        regexp: "[a-zA-Z0-9]{5,20}"
      },
      nigeriaNin: {
        type: "tel",
        maxLength: 11,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{11}"
      },
      panamaId: {
        type: "tel",
        maxLength: 10,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{1})/, "$1-").replace(/(.{5})/, "$1-").replace(/\.$|-$/, "");
        },
        regexp: "[0-9]{8}"
      },
      paraguayCi: {
        type: "tel",
        maxLength: 20,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{5,20}"
      },
      peruDni: {
        type: "tel",
        maxLength: 9,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{8,9}"
      },
      philipinesPsn: {
        type: "tel",
        maxLength: 14,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{4})/, "$1-").replace(/(.{12})/, "$1-").replace(/\.$|-$/, "");
        },
        regexp: "[0-9]{12}"
      },
      senegalCni: {
        type: "tel",
        maxLength: 17,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{13,17}"
      },
      southAfricaId: {
        type: "tel",
        maxLength: 13,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{13}"
      },
      tanzaniaId: {
        type: "tel",
        maxLength: 23,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{8})/, "$1-").replace(/(.{14})/, "$1-").replace(/(.{20})/, "$1-").replace(/\.$|-$/, "");
        },
        regexp: "[0-9]{20}"
      },
      thailandId: {
        type: "tel",
        maxLength: 17,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{1})/, "$1 ").replace(/(.{6})/, "$1 ").replace(/(.{12})/, "$1 ").replace(/(.{15})/, "$1 ").trim();
        },
        regexp: "[0-9]{13}"
      },
      turkeyTcKimlikNo: {
        type: "tel",
        maxLength: 20,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{5,20}"
      },
      ugandaNic: {
        type: "tel",
        maxLength: 14,
        mask: function (e) {
          return e.replace(/[^\da-zA-Z]/g, "").toUpperCase();
        },
        regexp: "[a-zA-Z0-9]{14}"
      },
      uriguayCi: {
        type: "tel",
        maxLength: 8,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{6,8}"
      },
      vietnamVnid: {
        type: "tel",
        maxLength: 12,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "^[0-9]{9}$|^[0-9]{12}$"
      },
      indianCustomerPhone: {
        type: "tel",
        maxLength: 15,
        regexp: "(\\+91[\\-\\s]?)?[0]?(91)?[789]\\d{9}",
        mask: function (e) {
          return e.replace(/[^+?\-?(?)?\d?]/, "");
        }
      },
      gbrPostalCode: {
        type: "tel",
        maxLength: 8,
        mask: function (e) {
          var t = e.replace(/[^\w]/gi, ""),
            n = new RegExp("^[0-9]{1,8}$").test(t),
            r = e.replace(/[^\w ]/g, "").trimStart().toUpperCase();
          return n ? r.slice(0, 5) : r;
        },
        regexp: function () {
          return "^(([A-Z]{1,2}\\d[A-Z\\d]?|ASCN|STHL|TDCU|BBND|[BFS]IQQ|PCRN|TKCA) ?\\d[A-Z]{2}|BFPO ?\\d{1,4}|(KY\\d|MSR|VG|AI)[ -]?\\d{4}|[A-Z]{2} ?\\d{2}|GE ?CX|GIR ?0A{2}|SAN ?TA1)$|^[0-9]{5}$";
        },
        isOptional: !0
      },
      brazilCustomerPhone: {
        type: "tel",
        maxLength: 10,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").trim();
        },
        regexp: "^[0-9]{5}[0-9]{5}$"
      },
      brazilZip: {
        type: "text",
        maxLength: 9,
        mask: function (e) {
          return e.replace(/[^\d]/g, "").replace(/(.{5})/, "$1-").replace(/\.$|-$/, "");
        },
        regexp: "[0-9]{8}"
      },
      indiaZip: {
        type: "tel",
        maxLength: 6,
        mask: function (e) {
          return e.replace(/[^\d]/g, "");
        },
        regexp: "[0-9]{6}"
      }
    },
    zC = function (e) {
      return e.Verve = "verve", e.Visa = "visa", e.Mastercard = "mastercard", e.Maestro = "maestro", e.AmericanExpress = "american-express", e.Jcb = "jcb", e.DinersClub = "diners-club", e.Discover = "discover", e.Aura = "aura", e.Elo = "elo", e.Hipercard = "hipercard", e.CartesBancaires = "cartes-bancaires", e.Rupay = "rupay", e.BCCard = "bc-card", e.UnionPay = "unionpay", e.Dankort = "dankort", e.GPNCard = "gpn-card", e.Troy = "troy", e.ThaiPaymentNetwork = "thai-payment-network", e.MADA = "mada", e.Bancontact = "bancontact", e.Interac = "interac", e.Bajaj = "bajaj", e;
    }(zC || {}),
    VC = function (e) {
      return e.Apple = "apple", e.Google = "google", e;
    }(VC || {}),
    qC = Object.keys(DC),
    $C = function () {
      function e(t, n, r, i) {
        var o = this;
        f(this, e), this.defaultMerchantName = n, this.callbacks = r, this.apiTransport = i, this.session = null, this.resolveElement = function () {
          return null;
        }, this.elementPromise = new Promise(function (e) {
          o.resolveElement = e;
        });
        var a = t.amount,
          s = t.countryCode,
          u = t.collectZipCode,
          c = t.currency,
          l = t.createSessionUrl,
          h = t.buttonColor,
          d = t.buttonType,
          p = t.language,
          g = t.merchantName,
          v = t.supportedNetworks,
          y = t.requiredShippingContactFields;
        this.merchantName = g || "", this.totalPrice = a, this.countryCode = s, this.currencyCode = c, this.buttonColor = h || e.defaultButtonColor, this.buttonType = d || e.defaultButtonType, this.language = p, this.createSessionUrl = l, this.supportedNetworks = v || e.supportedNetworks, this.merchantCapabilities = ["supports3DS"], this.requiredShippingContactFields = y, this.collectZipCode = u;
      }
      return d(e, [{
        key: "element",
        get: function () {
          return this.elementPromise;
        }
      }, {
        key: "init",
        value: function () {
          this.callbacks.beforeMount(), this.appendApplePayStyles();
          var t = document.createElement("div");
          t.id = e.buttonId, t.className = this.getButtonClassName(), t.onclick = this.onApplePayClick.bind(this), this.language && t.setAttribute("lang", this.language), this.resolveElement(t), this.callbacks.mounted();
        }
      }, {
        key: "destroy",
        value: function () {
          try {
            var e;
            null === (e = this.session) || void 0 === e || e.abort();
          } catch (t) {}
        }
      }, {
        key: "completePayment",
        value: function (e) {
          try {
            var t, n;
            if (e) null === (t = this.session) || void 0 === t || t.completePayment(ApplePaySession.STATUS_SUCCESS);else null === (n = this.session) || void 0 === n || n.completePayment(ApplePaySession.STATUS_FAILURE);
          } catch (r) {}
          this.session = null;
        }
      }, {
        key: "updateAmount",
        value: function (e) {
          this.totalPrice = String(e || 1);
        }
      }, {
        key: "updateCurrency",
        value: function (e) {
          this.currencyCode = e;
        }
      }, {
        key: "updateAppearance",
        value: function () {
          var t = l(s().mark(function t(n) {
            var r, i, o;
            return s().wrap(function (t) {
              for (;;) switch (t.prev = t.next) {
                case 0:
                  return t.next = 2, this.elementPromise;
                case 2:
                  (r = t.sent) && (i = n.buttonType, o = n.buttonColor, this.buttonColor = o || e.defaultButtonColor, this.buttonType = i || e.defaultButtonType, r.className = this.getButtonClassName(), r.removeAttribute("style"), this.appendApplePayStyles());
                case 4:
                case "end":
                  return t.stop();
              }
            }, t, this);
          }));
          return function (e) {
            return t.apply(this, arguments);
          };
        }()
      }, {
        key: "onValidateMerchant",
        value: function () {
          var e = l(s().mark(function e(t) {
            var n, r, i;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  return e.prev = 0, e.next = 3, this.apiTransport({
                    url: this.createSessionUrl,
                    method: "POST",
                    body: JSON.stringify({
                      validationUrl: t.validationURL,
                      domain: this.getTopWindowDomain()
                    })
                  });
                case 3:
                  return r = e.sent, e.next = 6, r.json();
                case 6:
                  (n = e.sent) && (null === (i = this.session) || void 0 === i || i.completeMerchantValidation(n), this.callbacks.pageOpened()), e.next = 14;
                  break;
                case 10:
                  e.prev = 10, e.t0 = e.catch(0), this.callbacks.pageClosed(), this.destroy();
                case 14:
                case "end":
                  return e.stop();
              }
            }, e, this, [[0, 10]]);
          }));
          return function (t) {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "onPaymentAuthorized",
        value: function () {
          var e = l(s().mark(function e(t) {
            var n;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  if (t.payment.token) this.callbacks.pay(a(a({}, t.payment.token), {}, {
                    shippingContact: t.payment.shippingContact,
                    billingContact: t.payment.billingContact
                  }));else try {
                    this.callbacks.pageClosed(), null === (n = this.session) || void 0 === n || n.completePayment(ApplePaySession.STATUS_FAILURE);
                  } catch (r) {}
                case 1:
                case "end":
                  return e.stop();
              }
            }, e, this);
          }));
          return function (t) {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "onApplePayClick",
        value: function () {
          var e = this,
            t = this.totalPrice,
            n = {
              countryCode: this.countryCode,
              currencyCode: this.currencyCode,
              supportedNetworks: this.supportedNetworks,
              merchantCapabilities: this.merchantCapabilities,
              requiredShippingContactFields: this.requiredShippingContactFields,
              total: {
                label: this.merchantName || this.defaultMerchantName,
                amount: t
              }
            };
          this.collectZipCode && (n.requiredBillingContactFields = ["postalAddress"]), this.callbacks.click && this.callbacks.click(), this.session = new ApplePaySession(3, n), this.session.begin(), this.session.onvalidatemerchant = this.onValidateMerchant.bind(this), this.session.onpaymentauthorized = this.onPaymentAuthorized.bind(this), this.session.oncancel = function () {
            e.session = null, e.callbacks.pageClosed();
          };
        }
      }, {
        key: "getApplePayStyles",
        value: function () {
          var e = ".apple-pay-button-".concat(this.buttonColor, " {\n      background-image: -webkit-named-image(apple-pay-logo-black);\n      background-color: white;\n      border: .5px solid black;\n    }"),
            t = ".apple-pay-button-".concat(this.buttonColor, " {\n      background-image: -webkit-named-image(apple-pay-logo-").concat("white" === this.buttonColor ? "black" : "white", ");\n      background-color: ").concat(this.buttonColor, ";\n    }");
          return "\n    p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 12.0px Helvetica; min-height: 14.0px}\n    p.p2 {margin: 0.0px 0.0px 0.0px 0.0px; font: 12.0px Helvetica}\n\n    @supports (-webkit-appearance: -apple-pay-button) {\n      .apple-pay-button {\n        cursor: pointer;\n        height: inherit;\n        border-radius: 4px;\n        -webkit-appearance: -apple-pay-button;\n        -apple-pay-button-type: ".concat(this.buttonType, ";\n      }\n      .apple-pay-button-").concat(this.buttonColor, " {\n        -apple-pay-button-style: ").concat(this.buttonColor, ";\n      }\n    }\n    @supports not (-webkit-appearance: -apple-pay-button) {\n      .apple-pay-button {\n        border-radius: 4px;\n        cursor: pointer;\n        background-size: 100% 60%;\n        background-repeat: no-repeat;\n        background-position: 50% 50%;\n        padding: 0;\n        box-sizing: border-box;\n        max-height: 640px;\n      }\n      ").concat("white-outline" === this.buttonColor ? e : t, "\n    }\n  ");
        }
      }, {
        key: "getButtonClassName",
        value: function () {
          return "apple-pay-button apple-pay-button-".concat(this.buttonColor);
        }
      }, {
        key: "appendApplePayStyles",
        value: function () {
          var t = document.getElementById(e.applePayCssId);
          t && t.remove();
          var n = document.createElement("style");
          n.id = e.applePayCssId, n.innerHTML = this.getApplePayStyles(), document.getElementsByTagName("head")[0].appendChild(n);
        }
      }, {
        key: "getTopWindowDomain",
        value: function () {
          var e;
          try {
            e = window.self !== window.top;
          } catch (n) {
            e = !0;
          }
          var t = e && document.referrer || window.location.href;
          return new URL(t).hostname;
        }
      }], [{
        key: "isPossibleToMakePayments",
        value: function () {
          var e = !1;
          try {
            var t;
            e = !!window.ApplePaySession && (null === (t = ApplePaySession) || void 0 === t ? void 0 : t.canMakePayments());
          } catch (n) {}
          return e;
        }
      }]);
    }();
  (UC = $C).applePayCssId = "apple-pay-style-id", UC.supportedNetworks = ["visa", "masterCard", "amex", "discover", "jcb"], UC.forbiddenTypes = ["donate", "support", "rent", "contribute", "tip"], UC.defaultButtonType = "default", UC.defaultButtonColor = "default", UC.buttonId = "apple-pay";
  var GC,
    HC = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, [e])).name = "GooglePayError", r;
      }
      return g(n, e), d(n);
    }(m(Error)),
    WC = function () {
      function e(t, n, r, i) {
        var o = this;
        f(this, e), this.buttonCss = n, this.callbacks = r, this.paymentsClient = null, this.baseRequest = {
          apiVersion: 2,
          apiVersionMinor: 0
        }, this.tokenizationSpecification = {
          type: "PAYMENT_GATEWAY",
          parameters: {
            gateway: atob("c29saWQ="),
            gatewayMerchantId: ""
          }
        }, this.logger = {
          error: function () {},
          warning: function () {},
          debug: function () {}
        }, this.resolveElement = function () {
          return null;
        }, this.rejectElement = function () {
          return null;
        }, this.elementPromise = new Promise(function (e, t) {
          o.resolveElement = e, o.rejectElement = t;
        });
        var a = t.amount,
          s = t.countryCode,
          u = t.currency,
          c = t.env,
          l = t.gatewayMerchantId,
          h = t.merchantId,
          d = t.merchantName,
          p = t.language,
          g = t.buttonColor,
          v = t.buttonType,
          y = t.allowedAuthMethods,
          m = t.emailRequired,
          b = t.zipCodeRequired;
        this.totalPrice = String(a), this.countryCode = s, this.currencyCode = u, this.env = c, this.merchantName = d, this.merchantId = h, this.language = p, this.buttonColor = g || "black", this.buttonType = v, this.emailRequired = m, this.zipCodeRequired = b, this.baseCardPaymentMethod = e.getBaseCardPaymentMethod(y), this.zipCodeRequired && (this.baseCardPaymentMethod.parameters.billingAddressRequired = !0, this.baseCardPaymentMethod.parameters.billingAddressParameters = {
          format: "MIN"
        }), this.tokenizationSpecification.parameters.gatewayMerchantId = l, i && (this.logger = i);
      }
      return d(e, [{
        key: "element",
        get: function () {
          return this.elementPromise;
        }
      }, {
        key: "init",
        value: function () {
          var t = this;
          this.callbacks.beforeMount();
          var n = "google-pay-script-id",
            r = document.getElementById(n);
          if (r) r.hasAttribute("loaded") ? this.onGooglePayLoaded() : r.addEventListener("load", function () {
            return t.onGooglePayLoaded();
          });else {
            var i = document.createElement("script");
            i.id = n, i.type = "text/javascript", i.src = e.src, i.async = !0, i.defer = !0, i.onload = function () {
              i.setAttribute("loaded", "true"), t.onGooglePayLoaded();
            }, i.onerror = function (e, n, r, o, a) {
              t.logger.error(new HC((a || e).toString()), {
                source: n,
                lineno: r,
                colno: o,
                googlePayScripLoaded: !1
              }), t.reject(), i.remove();
            };
            var o = document.getElementsByTagName("script")[0];
            o.parentNode.insertBefore(i, o);
            var a = document.createElement("style");
            a.innerHTML = this.buttonCss, document.getElementsByTagName("head")[0].appendChild(a);
          }
        }
      }, {
        key: "updateAmount",
        value: function (e) {
          this.totalPrice = String(e || 1);
        }
      }, {
        key: "updateCurrency",
        value: function (e) {
          this.currencyCode = e;
        }
      }, {
        key: "reject",
        value: function () {
          this.callbacks.mountFailed && this.callbacks.mountFailed(), this.rejectElement();
        }
      }, {
        key: "onGooglePayLoaded",
        value: function () {
          var e = l(s().mark(function e() {
            var t;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  if (google) {
                    e.next = 4;
                    break;
                  }
                  return this.logger.error(new HC("unable to load GooglePay")), this.reject(), e.abrupt("return");
                case 4:
                  return e.prev = 4, t = this.getGooglePaymentsClient(), e.next = 8, t.isReadyToPay(this.getGoogleIsReadyToPayRequest());
                case 8:
                  e.sent.result && (this.addGooglePayButton(), this.prefetchGooglePaymentData()), e.next = 16;
                  break;
                case 12:
                  e.prev = 12, e.t0 = e.catch(4), this.reject(), e.t0 instanceof Error && this.logger.error(new HC(e.t0.toString()), e.t0);
                case 16:
                case "end":
                  return e.stop();
              }
            }, e, this, [[4, 12]]);
          }));
          return function () {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "getGooglePaymentsClient",
        value: function () {
          return null === this.paymentsClient && (this.paymentsClient = new google.payments.api.PaymentsClient({
            environment: this.env
          })), this.paymentsClient;
        }
      }, {
        key: "getGoogleIsReadyToPayRequest",
        value: function () {
          return a(a({}, this.baseRequest), {}, {
            allowedPaymentMethods: [this.baseCardPaymentMethod]
          });
        }
      }, {
        key: "addGooglePayButton",
        value: function () {
          try {
            var e = this.getGooglePaymentsClient().createButton({
              onClick: this.onGooglePaymentButtonClicked.bind(this),
              buttonColor: this.buttonColor,
              buttonType: this.buttonType,
              buttonLocale: this.language,
              buttonSizeMode: "fill"
            });
            this.resolveElement(e), this.callbacks.mounted();
          } catch (t) {
            this.logger.error(t), this.rejectElement();
          }
        }
      }, {
        key: "onGooglePaymentButtonClicked",
        value: function () {
          var e = l(s().mark(function e() {
            var t, n, r;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  return (t = this.getGooglePaymentDataRequest()).transactionInfo = this.getGoogleTransactionInfo(), e.prev = 2, n = this.getGooglePaymentsClient(), this.callbacks.pageOpened(), e.next = 7, n.loadPaymentData(t);
                case 7:
                  r = e.sent, this.processPayment(r), e.next = 15;
                  break;
                case 11:
                  e.prev = 11, e.t0 = e.catch(2), e.t0 instanceof Error ? this.logger.error(e.t0) : this.logger.error(new HC("Unable to open google pay"), e.t0), this.callbacks.pageClosed();
                case 15:
                case "end":
                  return e.stop();
              }
            }, e, this, [[2, 11]]);
          }));
          return function () {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "getGoogleTransactionInfo",
        value: function () {
          return {
            countryCode: this.countryCode,
            currencyCode: this.currencyCode,
            totalPriceStatus: e.TotalPriceStatus.final,
            totalPriceLabel: "Total",
            totalPrice: this.totalPrice
          };
        }
      }, {
        key: "getGooglePaymentDataRequest",
        value: function () {
          return a(a({}, this.baseRequest), {}, {
            emailRequired: this.emailRequired,
            allowedPaymentMethods: [a(a({}, this.baseCardPaymentMethod), {}, {
              tokenizationSpecification: this.tokenizationSpecification
            })],
            transactionInfo: this.getGoogleTransactionInfo(),
            merchantInfo: {
              merchantName: this.merchantName,
              merchantId: this.merchantId
            }
          });
        }
      }, {
        key: "prefetchGooglePaymentData",
        value: function () {
          var t = this.getGooglePaymentDataRequest();
          t.transactionInfo = {
            totalPrice: "",
            totalPriceStatus: e.TotalPriceStatus.unknown,
            currencyCode: "USD"
          }, this.getGooglePaymentsClient().prefetchPaymentData(t);
        }
      }, {
        key: "processPayment",
        value: function (e) {
          var t;
          this.callbacks.pay(JSON.stringify(a(a({}, JSON.parse(e.paymentMethodData.tokenizationData.token)), {}, {
            email: e.email,
            billingAddress: (null === (t = e.paymentMethodData.info) || void 0 === t ? void 0 : t.billingAddress) || null
          })));
        }
      }], [{
        key: "getBaseCardPaymentMethod",
        value: function (e) {
          return {
            type: "CARD",
            parameters: {
              allowedAuthMethods: e || ["PAN_ONLY", "CRYPTOGRAM_3DS"],
              allowedCardNetworks: ["AMEX", "DISCOVER", "JCB", "MASTERCARD", "VISA"]
            }
          };
        }
      }, {
        key: "prefetch",
        value: function () {
          var e = "google-pay-prefetch-id";
          if (!document.getElementById(e)) {
            var t = document.createElement("link");
            t.rel = "prefetch", t.id = e, t.href = this.src, document.head.appendChild(t);
          }
        }
      }]);
    }();
  (GC = WC).TotalPriceStatus = {
    unknown: "NOT_CURRENTLY_KNOWN",
    final: "FINAL"
  }, GC.forbiddenTypes = ["donate", "book"], GC.src = "https://pay.google.com/gp/p/js/pay.js";
  var JC = va,
    ZC = ze,
    XC = rn;
  Si({
    target: "Reflect",
    stat: !0,
    forced: !A(function () {
      Reflect.apply(function () {});
    })
  }, {
    apply: function (e, t, n) {
      return JC(ZC(e), t, XC(n));
    }
  });
  var YC,
    KC = function () {
      var e = function () {},
        t = function () {},
        n = function () {
          return console.log("shippingAddressValidator is not defined. Use fallback flow - allow all addresses"), new Promise(function (e) {
            e({
              allow: !0
            });
          });
        },
        r = null,
        i = null,
        o = null,
        a = {},
        u = null,
        c = {},
        f = "checkout",
        h = "vault",
        d = "paypal-js-sdk",
        p = "order-started-processing",
        g = "order-approved",
        v = "order-processed",
        y = "order-already-processed",
        m = "button-ready",
        b = "button-click",
        w = "button-error",
        k = "button-cancel",
        P = "paypal_create_order_error",
        x = {},
        S = [p, g, v, y, m, b, w, k];
      function C(e, t) {
        o && o.dispatchEvent(new CustomEvent(e, {
          detail: t
        }));
      }
      function E(e) {
        if (e && e.stack && e.message) {
          var t = e.message;
          return -1 !== t.indexOf("RATE_LIMIT_REACHED") && (t = "RATE_LIMIT_REACHED.Too many requests. Blocked due to rate limiting"), {
            message: t
          };
        }
        return e || {
          message: "Unknown error"
        };
      }
      function T(e) {
        return e && e.stack && e.message ? e.message : e ? "Unknown error" : "No errors";
      }
      function O(e, t, o, c, d, x, S) {
        return "created" === c ? function (t, o) {
          var c = {
            label: "buynow",
            shape: "pill",
            color: "gold"
          };
          if (o && (["label", "shape", "color"].forEach(function (e) {
            o[e] && (c[e] = o[e]);
          }), ["height"].forEach(function (e) {
            o[e] && (c[e] = parseInt(o[e], 10));
          })), void 0 !== o.shippingAddrValidatorFn) {
            var y = o.shippingAddrValidatorFn;
            window[y] ? n = window[y] : console.error("Function for validate address '" + y + "' not found");
          }
          var O = "undefined",
            _ = {
              fundingSource: paypal.FUNDING.PAYPAL,
              style: c,
              onInit: function () {
                C(m, {}), A("payment_source_location_hostname", window.location.hostname), null !== x && function (e, t, n, r) {
                  try {
                    var i = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || null;
                    if (!r || !i || !i.getEntriesByType) return;
                    for (var o = i.getEntriesByType("resource"); o.length;) {
                      var a = o.shift();
                      if (a.name === r) {
                        A(e, a.duration.toString());
                        break;
                      }
                    }
                  } catch (s) {}
                }("paypal_script_load_time", 0, 0, x), function (e) {
                  var t = !0;
                  j(m) && (L(m, "mounted"), t = !1), e && e(t);
                }(S && S.onInit);
              },
              onClick: function () {
                !function (e) {
                  var t = !0;
                  j(b) && (L(b, "interaction"), t = !1), e && e(t);
                }(S && S.onClick);
              },
              createOrder: function () {
                if (e === f) return C(b, {}), t().then(function (e) {
                  return O = e.apmGateToken;
                }).then(function (e) {
                  return fetch(r + "/paypal-direct/api/" + e + "/createOrder", {
                    method: "post",
                    headers: {
                      "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                      fraudnet_session_id: d
                    })
                  });
                }).catch(function (e) {
                  throw A(P, T(e)), e;
                }).then(function (e) {
                  return e.json();
                }).then(function (e) {
                  if (null != e.id) return e.id;
                  if (null == e.id && null != e.error) {
                    var t = "Error creating order: " + e.error;
                    A(P, t), C(w, {
                      error: E(t)
                    }), S && S.onCreateOrderError && S.onCreateOrderError(t);
                  }
                  return null;
                });
              },
              createBillingAgreement: function () {
                if (e === h) return C(b, {}), t().then(function (e) {
                  return O = e.apmGateToken;
                }).then(function (e) {
                  return fetch(r + "/paypal-direct/api/" + e + "/createBaTmpToken", {
                    method: "post",
                    headers: {
                      "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                      fraudnet_session_id: d
                    })
                  });
                }).catch(function (e) {
                  throw A("paypal_create_ba_error", T(e)), e;
                }).then(function (e) {
                  return e.json();
                }).then(function (e) {
                  return e.token_id;
                });
              },
              onShippingChange: function () {
                var e = l(s().mark(function e(t, r) {
                  var i, o, u, c, l;
                  return s().wrap(function (e) {
                    for (;;) switch (e.prev = e.next) {
                      case 0:
                        if (S && S.onShippingChange && S.onShippingChange(), void 0 !== (c = a[t.shipping_address.country_code])) {
                          e.next = 5;
                          break;
                        }
                        return console.error("Unknown country code:", t.shipping_address.country_code), e.abrupt("return", r.reject());
                      case 5:
                        return l = {
                          country_a3: c.IsoCodeA3,
                          country_a2: t.shipping_address.country_code,
                          state: null !== (i = t.shipping_address.state) && void 0 !== i ? i : null,
                          city: null !== (o = t.shipping_address.city) && void 0 !== o ? o : null,
                          zip: null !== (u = t.shipping_address.postal_code) && void 0 !== u ? u : null
                        }, e.next = 8, n(l).then(function (e) {
                          return "object" != typeof e && (console.error("Unknown response from address validator. Result must be an object"), r.reject()), "boolean" != typeof e.allow && (console.error('Unknown response from address validator. Key "allow" must contain a boolean value'), r.reject()), e.allow ? r.resolve() : r.reject();
                        }).catch(function (e) {
                          console.error("Address validation error:", e), r.reject();
                        });
                      case 8:
                      case "end":
                        return e.stop();
                    }
                  }, e);
                }));
                return function (t, n) {
                  return e.apply(this, arguments);
                };
              }(),
              onApprove: function (t) {
                return e === f ? "continue" === u ? (R(S && S.onStartProcessing), fetch(r + "/paypal-direct/api/" + O + "/onApprove", {
                  method: "post",
                  headers: {
                    "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                    paypal_order_id: t.orderID
                  })
                }).then(function (e) {
                  return e.json();
                }).then(function (e) {
                  return C(g, {
                    data: e
                  }), S && S.onApprove && S.onApprove(), null;
                })) : (C(p, {}), R(S && S.onStartProcessing), fetch(r + "/paypal-direct/api/" + O + "/captureOrder", {
                  method: "post",
                  headers: {
                    "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                    paypal_order_id: t.orderID,
                    fraudnet_session_id: d
                  })
                }).then(function (e) {
                  return e.json();
                }).then(function (e) {
                  return console.log("Transaction completed"), C(v, {
                    data: e
                  }), B(S && S.onOrderProcessed), null;
                })) : e === h ? (C(p, {}), R(S && S.onStartProcessing), fetch(r + "/paypal-direct/api/" + O + "/createBaAndPay", {
                  method: "post",
                  headers: {
                    "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                    billing_agreement_tmp_token: t.billingToken,
                    fraudnet_session_id: d
                  })
                }).then(function (e) {
                  return e.json();
                }).then(function (e) {
                  return C(v, {
                    data: e
                  }), B(S && S.onOrderProcessed), console.log("Transaction completed"), null;
                })) : void 0;
              },
              onError: function (e) {
                if (console.log("error", e), A("paypal_button_error", T(e)), !(e && "Expected an order id to be passed" === e.message || e && "Detected popup close" === e.message || e && "Component closed" === e.message || e && "Document is ready and element #paypal-button does not exist" === e.message)) return I(e), fetch(r + "/paypal-direct/api/" + O + "/processDeclineFlow", {
                  method: "post",
                  headers: {
                    "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                    error_message: JSON.stringify(E(e))
                  })
                });
              },
              onCancel: function () {
                console.log("raise on_cancel"), A("paypal_button_cancel"), C(k, {}), S && S.onCancel && S.onCancel();
              }
            };
          return e === h && delete _.createOrder, e === f && delete _.createBillingAgreement, paypal.Buttons(_).render("#" + i);
        }(t, o) : (C(y, {}), Promise.resolve());
      }
      function I(t) {
        try {
          e(t);
        } catch (n) {
          console.log(n);
        }
      }
      function A(e, n) {
        if (c && c.entityName && c.entityValue && c.signature) {
          var r = {
            category: "direct_paypal_button",
            level: "button_loading",
            entity_name: c.entityName,
            entity_value: c.entityValue,
            event_time: new Date().toISOString()
          };
          "undefined" !== n && (r.value = n), t(e, r, c.signature);
        }
      }
      function L(e, t) {
        console.error("The PayPal button event '".concat(e, "' is outdated and will be removed in future releases.\nPlease use regular event by subscribing to it via 'sdk.on(\"").concat(t, "\", handler)'.\nSee more in the 'Form Events' section of the documentation.\n%cThe original, 'sdk.on(\"").concat(t, "\", handler)', event will not be called to prevent duplicates.%c"), "font-weight: bold", "font-weight: normal");
      }
      function j(e) {
        return S.includes(e) && x[e] && x[e] > 0;
      }
      function R(e) {
        var t = !0;
        j(p) && (L(p, "submit"), t = !1), e && e(t);
      }
      function B(e) {
        var t = !0;
        j(v) && (L(v, "success/fail"), t = !1), e && e(t);
      }
      return {
        addExceptionListener: function (t) {
          e = t;
        },
        addTrackEventListener: function (e) {
          t = e;
        },
        setCountryParams: function (e) {
          a = e;
        },
        updateCurrency: function (e) {
          var t = document.getElementById(d);
          if (t) {
            var n = t.src;
            if (n.includes("currency=")) {
              var r = n.replace(/currency=([A-Z]{3})/, "currency=" + e);
              t.src = r;
            }
          }
        },
        initSdkV1: function (e, t, n, a, s, l, p, g) {
          return new Promise(function (v, y) {
            r = e.replace(/\/$/, ""), i = t;
            var m = {
              apply: function (e, t, n) {
                var r = n[0];
                return S.includes(r) && (!function (e) {
                  void 0 === x[e] ? x[e] = 1 : x[e]++;
                }(r), console.error("The PayPal button event '".concat(r, "' is outdated and will be removed in future releases.\nPlease use regular form events by subscribing to them via 'sdk.on(eventName, handler)'.\nSee more in the 'Form Events' section of the documentation."))), Reflect.apply(e, t, n);
              }
            };
            (o = document.getElementById(t)).addEventListener = new Proxy(o.addEventListener, m);
            try {
              var b = "https://www.paypal.com/sdk/js?client-id=" + a.clientId + "&components=buttons,funding-eligibility";
              a.flow === h && (b += "&vault=true&intent=tokenize"), a.flow === f && (b += "&intent=capture", b += "&currency=" + s.currency), b += "continue" === (u = s.paymentMethodData.userAction) ? "&commit=false" : "&commit=true", a.merchantId && (b += "&merchant-id=" + a.merchantId), c = s.trackData, function (e) {
                return new Promise(function (t, n) {
                  var r = document.createElement("script");
                  r.src = e, r.type = "text/javascript", r.defer = !0, r.async = !0, r.id = d, document.getElementsByTagName("head").item(0).appendChild(r), r.onload = function () {
                    t();
                  }, r.onerror = function (e, t, r, i, o) {
                    n(o ? "PayPal SDK script error: " + o.toString() : new Error("Failed to load PayPal SDK script"));
                  };
                });
              }(b).then(function () {
                var e = O(a.flow, p, n, s.spOrderStatus, s.fraudnetSessionId, l, g).catch(function (e) {
                    throw A("paypal_button_general_error", T(e)), I(e), C(w, {
                      error: E(e)
                    }), e;
                  }),
                  t = function (e, t) {
                    var n = {
                      f: t,
                      s: "SGATE_WIDGET_PAY_BTN",
                      sandbox: e
                    };
                    return new Promise(function (e) {
                      for (var t = document.querySelectorAll("[fncls=fnparams-dede7cc5-15fd-4c75-a9f4-36c430ee3a99]"), r = 0; r < t.length; r++) t[r].remove();
                      var i = document.createElement("script");
                      i.append(JSON.stringify(n)), i.type = "application/json", i.setAttribute("fncls", "fnparams-dede7cc5-15fd-4c75-a9f4-36c430ee3a99"), document.getElementsByTagName("head").item(0).appendChild(i), e();
                    });
                  }(a.sandbox, s.fraudnetSessionId).then(function () {
                    return function () {
                      return new Promise(function (e, t) {
                        var n = document.createElement("script");
                        n.src = "https://c.paypal.com/da/r/fb.js", n.type = "text/javascript", document.getElementsByTagName("head").item(0).appendChild(n), n.onload = function () {
                          e();
                        }, n.onerror = function (e, n, r, i, o) {
                          t(o ? "PayPal FraudNet script error: " + o.toString() : new Error("Failed to load PayPal FraudNet script"));
                        };
                      });
                    }().then(function () {
                      console.log("FraudNet loaded successfully");
                    });
                  });
                return Promise.all([e, t]);
              }).then(function () {
                v();
              }).catch(function (e) {
                y(e);
              });
            } catch (k) {
              I(k), y(k);
            }
          });
        }
      };
    }();
  window.apmGatePayPalSdk = KC;
  var QC = function () {
    function e(t, n) {
      var r = this;
      f(this, e), this.paypalData = t, this.callbacks = n, this.sdkLoaded = !1, this.resolveElement = function () {
        return null;
      }, this.elementPromise = new Promise(function (e) {
        r.resolveElement = e;
      }), this.prepareOrder = l(s().mark(function e() {
        var t, n, i;
        return s().wrap(function (e) {
          for (;;) switch (e.prev = e.next) {
            case 0:
              return t = r.callbacks.onCreateOrder, e.next = 3, t();
            case 3:
              return n = e.sent, i = n.token, e.abrupt("return", {
                apmGateToken: i
              });
            case 6:
            case "end":
              return e.stop();
          }
        }, e);
      }));
    }
    return d(e, [{
      key: "element",
      get: function () {
        return this.elementPromise;
      }
    }, {
      key: "init",
      value: function () {
        var t = document.createElement("div");
        t.id = e.containerId, t.className = e.className, this.resolveElement(t);
      }
    }, {
      key: "appendButton",
      value: function () {
        var t = l(s().mark(function t() {
          var n, r, i, o, a, u, c;
          return s().wrap(function (t) {
            for (;;) switch (t.prev = t.next) {
              case 0:
                if (!this.sdkLoaded) {
                  t.next = 2;
                  break;
                }
                return t.abrupt("return");
              case 2:
                return n = this.paypalData, r = n.baseApiPath, i = n.credentials, o = n.appearance, a = n.currency, u = n.userAction, c = n.antifraud, KC.addExceptionListener(this.callbacks.onError), t.next = 6, KC.initSdkV1(r, e.containerId, {
                  label: null == o ? void 0 : o.label,
                  shape: null == o ? void 0 : o.shape,
                  color: null == o ? void 0 : o.color,
                  height: null == o ? void 0 : o.height
                }, i, {
                  currency: a,
                  spOrderStatus: "created",
                  fraudnetSessionId: c.sessionId,
                  paymentMethodData: {
                    userAction: u
                  }
                }, null, this.prepareOrder, this.callbacks);
              case 6:
                this.sdkLoaded = !0;
              case 7:
              case "end":
                return t.stop();
            }
          }, t, this);
        }));
        return function () {
          return t.apply(this, arguments);
        };
      }()
    }, {
      key: "updateCurrency",
      value: function (e) {
        this.paypalData.currency = e;
        try {
          KC.updateCurrency(e);
        } catch (UO) {
          this.callbacks.onError(UO);
        }
      }
    }]);
  }();
  (YC = QC).containerId = "paypal-button", YC.className = "paypal-button";
  var eE = O,
    tE = W(1..valueOf),
    nE = Si,
    rE = L,
    iE = O,
    oE = eE,
    aE = W,
    sE = vi,
    uE = ft,
    cE = Ad,
    lE = ye,
    fE = _e,
    hE = Rt,
    dE = A,
    pE = xr.f,
    gE = I.f,
    vE = Kt.f,
    yE = tE,
    mE = iS.trim,
    bE = "Number",
    wE = iE[bE];
  oE[bE];
  var kE = wE.prototype,
    PE = iE.TypeError,
    xE = aE("".slice),
    SE = aE("".charCodeAt),
    CE = function (e) {
      var t,
        n,
        r,
        i,
        o,
        a,
        s,
        u,
        c = hE(e, "number");
      if (fE(c)) throw new PE("Cannot convert a Symbol value to a number");
      if ("string" == typeof c && c.length > 2) if (c = mE(c), 43 === (t = SE(c, 0)) || 45 === t) {
        if (88 === (n = SE(c, 2)) || 120 === n) return NaN;
      } else if (48 === t) {
        switch (SE(c, 1)) {
          case 66:
          case 98:
            r = 2, i = 49;
            break;
          case 79:
          case 111:
            r = 8, i = 55;
            break;
          default:
            return +c;
        }
        for (a = (o = xE(c, 2)).length, s = 0; s < a; s++) if ((u = SE(o, s)) < 48 || u > i) return NaN;
        return parseInt(o, r);
      }
      return +c;
    },
    EE = sE(bE, !wE(" 0o1") || !wE("0b1") || wE("+0x1")),
    TE = function (e) {
      var t = arguments.length < 1 ? 0 : wE(function (e) {
        var t = hE(e, "number");
        return "bigint" == typeof t ? t : CE(t);
      }(e));
      return function (e) {
        return lE(kE, e) && dE(function () {
          yE(e);
        });
      }(this) ? cE(Object(t), this, TE) : t;
    };
  TE.prototype = kE, EE && (kE.constructor = TE), nE({
    global: !0,
    constructor: !0,
    wrap: !0,
    forced: EE
  }, {
    Number: TE
  });
  EE && function (e, t) {
    for (var n, r = rE ? pE(t) : "MAX_VALUE,MIN_VALUE,NaN,NEGATIVE_INFINITY,POSITIVE_INFINITY,EPSILON,MAX_SAFE_INTEGER,MIN_SAFE_INTEGER,isFinite,isInteger,isNaN,isSafeInteger,parseFloat,parseInt,fromString,range".split(","), i = 0; r.length > i; i++) uE(t, n = r[i]) && !uE(e, n) && vE(e, n, gE(t, n));
  }(oE[bE], wE);
  var OE = "undefined" != typeof globalThis && globalThis || "undefined" != typeof self && self || "undefined" != typeof global && global || {},
    IE = ("URLSearchParams" in OE),
    AE = "Symbol" in OE && "iterator" in Symbol,
    LE = "FileReader" in OE && "Blob" in OE && function () {
      try {
        return new Blob(), !0;
      } catch (e) {
        return !1;
      }
    }(),
    jE = ("FormData" in OE),
    RE = ("ArrayBuffer" in OE);
  if (RE) var BE = ["[object Int8Array]", "[object Uint8Array]", "[object Uint8ClampedArray]", "[object Int16Array]", "[object Uint16Array]", "[object Int32Array]", "[object Uint32Array]", "[object Float32Array]", "[object Float64Array]"],
    _E = ArrayBuffer.isView || function (e) {
      return e && BE.indexOf(Object.prototype.toString.call(e)) > -1;
    };
  function NE(e) {
    if ("string" != typeof e && (e = String(e)), /[^a-z0-9\-#$%&'*+.^_`|~!]/i.test(e) || "" === e) throw new TypeError('Invalid character in header field name: "' + e + '"');
    return e.toLowerCase();
  }
  function FE(e) {
    return "string" != typeof e && (e = String(e)), e;
  }
  function ME(e) {
    var t = {
      next: function () {
        var t = e.shift();
        return {
          done: void 0 === t,
          value: t
        };
      }
    };
    return AE && (t[Symbol.iterator] = function () {
      return t;
    }), t;
  }
  function UE(e) {
    this.map = {}, e instanceof UE ? e.forEach(function (e, t) {
      this.append(t, e);
    }, this) : Array.isArray(e) ? e.forEach(function (e) {
      if (2 != e.length) throw new TypeError("Headers constructor: expected name/value pair to be length 2, found" + e.length);
      this.append(e[0], e[1]);
    }, this) : e && Object.getOwnPropertyNames(e).forEach(function (t) {
      this.append(t, e[t]);
    }, this);
  }
  function DE(e) {
    if (!e._noBody) return e.bodyUsed ? Promise.reject(new TypeError("Already read")) : void (e.bodyUsed = !0);
  }
  function zE(e) {
    return new Promise(function (t, n) {
      e.onload = function () {
        t(e.result);
      }, e.onerror = function () {
        n(e.error);
      };
    });
  }
  function VE(e) {
    var t = new FileReader(),
      n = zE(t);
    return t.readAsArrayBuffer(e), n;
  }
  function qE(e) {
    if (e.slice) return e.slice(0);
    var t = new Uint8Array(e.byteLength);
    return t.set(new Uint8Array(e)), t.buffer;
  }
  function $E() {
    return this.bodyUsed = !1, this._initBody = function (e) {
      this.bodyUsed = this.bodyUsed, this._bodyInit = e, e ? "string" == typeof e ? this._bodyText = e : LE && Blob.prototype.isPrototypeOf(e) ? this._bodyBlob = e : jE && FormData.prototype.isPrototypeOf(e) ? this._bodyFormData = e : IE && URLSearchParams.prototype.isPrototypeOf(e) ? this._bodyText = e.toString() : RE && LE && function (e) {
        return e && DataView.prototype.isPrototypeOf(e);
      }(e) ? (this._bodyArrayBuffer = qE(e.buffer), this._bodyInit = new Blob([this._bodyArrayBuffer])) : RE && (ArrayBuffer.prototype.isPrototypeOf(e) || _E(e)) ? this._bodyArrayBuffer = qE(e) : this._bodyText = e = Object.prototype.toString.call(e) : (this._noBody = !0, this._bodyText = ""), this.headers.get("content-type") || ("string" == typeof e ? this.headers.set("content-type", "text/plain;charset=UTF-8") : this._bodyBlob && this._bodyBlob.type ? this.headers.set("content-type", this._bodyBlob.type) : IE && URLSearchParams.prototype.isPrototypeOf(e) && this.headers.set("content-type", "application/x-www-form-urlencoded;charset=UTF-8"));
    }, LE && (this.blob = function () {
      var e = DE(this);
      if (e) return e;
      if (this._bodyBlob) return Promise.resolve(this._bodyBlob);
      if (this._bodyArrayBuffer) return Promise.resolve(new Blob([this._bodyArrayBuffer]));
      if (this._bodyFormData) throw new Error("could not read FormData body as blob");
      return Promise.resolve(new Blob([this._bodyText]));
    }), this.arrayBuffer = function () {
      if (this._bodyArrayBuffer) {
        var e = DE(this);
        return e || (ArrayBuffer.isView(this._bodyArrayBuffer) ? Promise.resolve(this._bodyArrayBuffer.buffer.slice(this._bodyArrayBuffer.byteOffset, this._bodyArrayBuffer.byteOffset + this._bodyArrayBuffer.byteLength)) : Promise.resolve(this._bodyArrayBuffer));
      }
      if (LE) return this.blob().then(VE);
      throw new Error("could not read as ArrayBuffer");
    }, this.text = function () {
      var e = DE(this);
      if (e) return e;
      if (this._bodyBlob) return function (e) {
        var t = new FileReader(),
          n = zE(t),
          r = /charset=([A-Za-z0-9_-]+)/.exec(e.type),
          i = r ? r[1] : "utf-8";
        return t.readAsText(e, i), n;
      }(this._bodyBlob);
      if (this._bodyArrayBuffer) return Promise.resolve(function (e) {
        for (var t = new Uint8Array(e), n = new Array(t.length), r = 0; r < t.length; r++) n[r] = String.fromCharCode(t[r]);
        return n.join("");
      }(this._bodyArrayBuffer));
      if (this._bodyFormData) throw new Error("could not read FormData body as text");
      return Promise.resolve(this._bodyText);
    }, jE && (this.formData = function () {
      return this.text().then(WE);
    }), this.json = function () {
      return this.text().then(JSON.parse);
    }, this;
  }
  UE.prototype.append = function (e, t) {
    e = NE(e), t = FE(t);
    var n = this.map[e];
    this.map[e] = n ? n + ", " + t : t;
  }, UE.prototype.delete = function (e) {
    delete this.map[NE(e)];
  }, UE.prototype.get = function (e) {
    return e = NE(e), this.has(e) ? this.map[e] : null;
  }, UE.prototype.has = function (e) {
    return this.map.hasOwnProperty(NE(e));
  }, UE.prototype.set = function (e, t) {
    this.map[NE(e)] = FE(t);
  }, UE.prototype.forEach = function (e, t) {
    for (var n in this.map) this.map.hasOwnProperty(n) && e.call(t, this.map[n], n, this);
  }, UE.prototype.keys = function () {
    var e = [];
    return this.forEach(function (t, n) {
      e.push(n);
    }), ME(e);
  }, UE.prototype.values = function () {
    var e = [];
    return this.forEach(function (t) {
      e.push(t);
    }), ME(e);
  }, UE.prototype.entries = function () {
    var e = [];
    return this.forEach(function (t, n) {
      e.push([n, t]);
    }), ME(e);
  }, AE && (UE.prototype[Symbol.iterator] = UE.prototype.entries);
  var GE = ["CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE"];
  function HE(e, t) {
    if (!(this instanceof HE)) throw new TypeError('Please use the "new" operator, this DOM object constructor cannot be called as a function.');
    var n = (t = t || {}).body;
    if (e instanceof HE) {
      if (e.bodyUsed) throw new TypeError("Already read");
      this.url = e.url, this.credentials = e.credentials, t.headers || (this.headers = new UE(e.headers)), this.method = e.method, this.mode = e.mode, this.signal = e.signal, n || null == e._bodyInit || (n = e._bodyInit, e.bodyUsed = !0);
    } else this.url = String(e);
    if (this.credentials = t.credentials || this.credentials || "same-origin", !t.headers && this.headers || (this.headers = new UE(t.headers)), this.method = function (e) {
      var t = e.toUpperCase();
      return GE.indexOf(t) > -1 ? t : e;
    }(t.method || this.method || "GET"), this.mode = t.mode || this.mode || null, this.signal = t.signal || this.signal || function () {
      if ("AbortController" in OE) return new AbortController().signal;
    }(), this.referrer = null, ("GET" === this.method || "HEAD" === this.method) && n) throw new TypeError("Body not allowed for GET or HEAD requests");
    if (this._initBody(n), !("GET" !== this.method && "HEAD" !== this.method || "no-store" !== t.cache && "no-cache" !== t.cache)) {
      var r = /([?&])_=[^&]*/;
      if (r.test(this.url)) this.url = this.url.replace(r, "$1_=" + new Date().getTime());else {
        this.url += (/\?/.test(this.url) ? "&" : "?") + "_=" + new Date().getTime();
      }
    }
  }
  function WE(e) {
    var t = new FormData();
    return e.trim().split("&").forEach(function (e) {
      if (e) {
        var n = e.split("="),
          r = n.shift().replace(/\+/g, " "),
          i = n.join("=").replace(/\+/g, " ");
        t.append(decodeURIComponent(r), decodeURIComponent(i));
      }
    }), t;
  }
  function JE(e) {
    var t = new UE();
    return e.replace(/\r?\n[\t ]+/g, " ").split("\r").map(function (e) {
      return 0 === e.indexOf("\n") ? e.substr(1, e.length) : e;
    }).forEach(function (e) {
      var n = e.split(":"),
        r = n.shift().trim();
      if (r) {
        var i = n.join(":").trim();
        try {
          t.append(r, i);
        } catch (UO) {
          console.warn("Response " + UO.message);
        }
      }
    }), t;
  }
  function ZE(e, t) {
    if (!(this instanceof ZE)) throw new TypeError('Please use the "new" operator, this DOM object constructor cannot be called as a function.');
    if (t || (t = {}), this.type = "default", this.status = void 0 === t.status ? 200 : t.status, this.status < 200 || this.status > 599) throw new RangeError("Failed to construct 'Response': The status provided (0) is outside the range [200, 599].");
    this.ok = this.status >= 200 && this.status < 300, this.statusText = void 0 === t.statusText ? "" : "" + t.statusText, this.headers = new UE(t.headers), this.url = t.url || "", this._initBody(e);
  }
  HE.prototype.clone = function () {
    return new HE(this, {
      body: this._bodyInit
    });
  }, $E.call(HE.prototype), $E.call(ZE.prototype), ZE.prototype.clone = function () {
    return new ZE(this._bodyInit, {
      status: this.status,
      statusText: this.statusText,
      headers: new UE(this.headers),
      url: this.url
    });
  }, ZE.error = function () {
    var e = new ZE(null, {
      status: 200,
      statusText: ""
    });
    return e.ok = !1, e.status = 0, e.type = "error", e;
  };
  var XE = [301, 302, 303, 307, 308];
  ZE.redirect = function (e, t) {
    if (-1 === XE.indexOf(t)) throw new RangeError("Invalid status code");
    return new ZE(null, {
      status: t,
      headers: {
        location: e
      }
    });
  };
  var YE = OE.DOMException;
  try {
    new YE();
  } catch (DO) {
    (YE = function (e, t) {
      this.message = e, this.name = t;
      var n = Error(e);
      this.stack = n.stack;
    }).prototype = Object.create(Error.prototype), YE.prototype.constructor = YE;
  }
  function KE(e, t) {
    return new Promise(function (n, r) {
      var i = new HE(e, t);
      if (i.signal && i.signal.aborted) return r(new YE("Aborted", "AbortError"));
      var o = new XMLHttpRequest();
      function a() {
        o.abort();
      }
      if (o.onload = function () {
        var e = {
          statusText: o.statusText,
          headers: JE(o.getAllResponseHeaders() || "")
        };
        0 === i.url.indexOf("file://") && (o.status < 200 || o.status > 599) ? e.status = 200 : e.status = o.status, e.url = "responseURL" in o ? o.responseURL : e.headers.get("X-Request-URL");
        var t = "response" in o ? o.response : o.responseText;
        setTimeout(function () {
          n(new ZE(t, e));
        }, 0);
      }, o.onerror = function () {
        setTimeout(function () {
          r(new TypeError("Network request failed"));
        }, 0);
      }, o.ontimeout = function () {
        setTimeout(function () {
          r(new TypeError("Network request timed out"));
        }, 0);
      }, o.onabort = function () {
        setTimeout(function () {
          r(new YE("Aborted", "AbortError"));
        }, 0);
      }, o.open(i.method, function (e) {
        try {
          return "" === e && OE.location.href ? OE.location.href : e;
        } catch (t) {
          return e;
        }
      }(i.url), !0), "include" === i.credentials ? o.withCredentials = !0 : "omit" === i.credentials && (o.withCredentials = !1), "responseType" in o && (LE ? o.responseType = "blob" : RE && (o.responseType = "arraybuffer")), t && "object" == typeof t.headers && !(t.headers instanceof UE || OE.Headers && t.headers instanceof OE.Headers)) {
        var s = [];
        Object.getOwnPropertyNames(t.headers).forEach(function (e) {
          s.push(NE(e)), o.setRequestHeader(e, FE(t.headers[e]));
        }), i.headers.forEach(function (e, t) {
          -1 === s.indexOf(t) && o.setRequestHeader(t, e);
        });
      } else i.headers.forEach(function (e, t) {
        o.setRequestHeader(t, e);
      });
      i.signal && (i.signal.addEventListener("abort", a), o.onreadystatechange = function () {
        4 === o.readyState && i.signal.removeEventListener("abort", a);
      }), o.send(void 0 === i._bodyInit ? null : i._bodyInit);
    });
  }
  KE.polyfill = !0, OE.fetch || (OE.fetch = KE, OE.Headers = UE, OE.Request = HE, OE.Response = ZE);
  var QE = function () {
      return d(function e(t) {
        var n = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {
          times: 5,
          time: 2e3,
          whenOnline: !0
        };
        f(this, e), this.requestInit = t, this.config = n, this.shouldRepeat = function (e) {
          return null === e || e >= 300;
        }, this.shouldRepeat = n.shouldRepeat || this.shouldRepeat;
      }, [{
        key: "execute",
        value: function () {
          return this.doRequest(this.requestInit, this.config);
        }
      }, {
        key: "isOnline",
        value: function () {
          return "undefined" == typeof window || !("onLine" in window.navigator) || window.navigator.onLine;
        }
      }, {
        key: "doRequest",
        value: function () {
          var e = l(s().mark(function e(t, n) {
            var r;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  if (!(n.times < 0)) {
                    e.next = 2;
                    break;
                  }
                  return e.abrupt("return", Promise.reject());
                case 2:
                  if (!this.config.whenOnline || this.isOnline() || !this.shouldRepeat(null)) {
                    e.next = 4;
                    break;
                  }
                  return e.abrupt("return", this.repeatWhenOnline(t, n));
                case 4:
                  return e.prev = 4, e.next = 7, fetch(t.url, t);
                case 7:
                  r = e.sent, e.next = 13;
                  break;
                case 10:
                  e.prev = 10, e.t0 = e.catch(4), r = {
                    ok: !1
                  };
                case 13:
                  if (!this.shouldRepeat(r.status || null)) {
                    e.next = 18;
                    break;
                  }
                  return e.abrupt("return", this.repeatWithTimeout(t, n));
                case 18:
                  return e.abrupt("return", r);
                case 19:
                case "end":
                  return e.stop();
              }
            }, e, this, [[4, 10]]);
          }));
          return function (t, n) {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "repeatWithTimeout",
        value: function (e, t) {
          var n = this;
          return new Promise(function (r, i) {
            setTimeout(function () {
              return n.doRequest(e, a(a({}, t), {}, {
                times: t.times - 1,
                time: 2 * t.time
              })).then(r).catch(i);
            }, Math.min(t.time, t.maxTime || Number.POSITIVE_INFINITY));
          });
        }
      }, {
        key: "repeatWhenOnline",
        value: function (e, t) {
          var n = this;
          return new Promise(function (r, i) {
            window.addEventListener("online", function () {
              n.doRequest(e, t).then(r).catch(i);
            }, {
              once: !0
            });
          });
        }
      }]);
    }(),
    eT = function (e) {
      return e.ApplePay = "applebtn", e.GooglePay = "googlebtn", e.Paypal = "paypal", e.Form = "form", e.Resign = "resign", e;
    }(eT || {}),
    tT = function (e) {
      return !!e.token;
    },
    nT = function () {
      function e(t, n, r, i, o, a, s, u, c) {
        f(this, e), this.configuration = t, this.token = n, this.release = r, this.paymentButtonsView = i, this.iframe = o, this.tracking = a, this.logger = s, this.interactionsNotifier = u, this.messageBus = c, this.isDestroyed = !1, this.applePay = null, this.googlePay = null, this.paypal = null;
      }
      return d(e, [{
        key: "getGooglePayData",
        value: function () {
          var e = this.configuration.clientSide.google,
            t = this.configuration.wallets.google;
          if (this.paymentButtonsView.canAppend(e) && null != t && t.merchantId) {
            var n,
              r = null == e ? void 0 : e.type,
              i = null !== (n = null == e ? void 0 : e.allowedAuthMethods) && void 0 !== n ? n : [],
              o = r && !Object.values(WC.forbiddenTypes).includes(r);
            return a(a({}, t), {}, {
              language: this.configuration.language,
              buttonColor: null == e ? void 0 : e.color,
              buttonType: o ? e.type : void 0,
              allowedAuthMethods: 0 === i.length ? ["PAN_ONLY", "CRYPTOGRAM_3DS"] : i,
              zipCodeRequired: this.configuration.collect.zip,
              emailRequired: this.configuration.collect.email
            });
          }
          return null;
        }
      }, {
        key: "getApplePayData",
        value: function () {
          var e = this.configuration.clientSide.apple,
            t = this.configuration.wallets.apple;
          if (this.paymentButtonsView.canAppend(e) && $C.isPossibleToMakePayments() && null != t && t.amount) {
            var n = null == e ? void 0 : e.type,
              r = n && !Object.values($C.forbiddenTypes).includes(n);
            return a(a({}, t), {}, {
              language: this.configuration.language,
              createSessionUrl: this.configuration.app.apple.createSessionUrl,
              buttonColor: null == e ? void 0 : e.color,
              collectZipCode: this.configuration.collect.zip,
              requiredShippingContactFields: this.configuration.collect.email ? ["email"] : void 0,
              buttonType: r ? n : "plain"
            });
          }
          return null;
        }
      }, {
        key: "getPaypalData",
        value: function () {
          var e = this.configuration.clientSide.paypal,
            t = this.configuration.wallets.paypal;
          return e && e.enabled && this.paymentButtonsView.canAppend(e) && t ? {
            baseApiPath: this.configuration.app.paypal.baseApiPath,
            credentials: {
              clientId: t.clientId,
              merchantId: t.merchantId,
              flow: t.flow,
              sandbox: t.sandbox
            },
            currency: t.currency,
            antifraud: {
              sessionId: t.fraudnetSessionId
            },
            appearance: {
              label: null == e ? void 0 : e.label,
              shape: null == e ? void 0 : e.shape,
              color: null == e ? void 0 : e.color,
              height: null == e ? void 0 : e.height
            }
          } : null;
        }
      }, {
        key: "resize",
        value: function () {
          var e;
          null === (e = this.paymentButtonsView) || void 0 === e || e.resize();
        }
      }, {
        key: "completeApplePayment",
        value: function (e) {
          var t;
          null === (t = this.applePay) || void 0 === t || t.completePayment(e);
        }
      }, {
        key: "update",
        value: function (e) {
          e.price && this.updatePrice(e.price), e.appearance && this.updateAppearance(e.appearance);
        }
      }, {
        key: "updatePrice",
        value: function (e) {
          var t,
            n,
            r,
            i,
            o,
            a = e.amount,
            s = e.currency;
          null === (t = this.applePay) || void 0 === t || t.updateAmount(a), null === (n = this.applePay) || void 0 === n || n.updateCurrency(s), null === (r = this.googlePay) || void 0 === r || r.updateAmount(a), null === (i = this.googlePay) || void 0 === i || i.updateCurrency(s), null === (o = this.paypal) || void 0 === o || o.updateCurrency(s);
        }
      }, {
        key: "updateAppearance",
        value: function (e) {
          if (e.applePay) {
            var t,
              n = e.applePay,
              r = n.buttonColor,
              i = n.buttonType;
            null === (t = this.applePay) || void 0 === t || t.updateAppearance({
              buttonColor: r,
              buttonType: i
            });
          }
        }
      }, {
        key: "setIsDisabled",
        value: function (e) {
          this.paymentButtonsView.setIsDisabled(e);
        }
      }, {
        key: "destroy",
        value: function () {
          this.isDestroyed = !0, this.clear();
        }
      }, {
        key: "appendPaymentButtons",
        value: function () {
          var e = this;
          this.clear();
          var t = this.getGooglePayData(),
            n = this.getApplePayData(),
            r = this.getPaypalData(),
            i = {};
          return t && (i.googlePay = new Promise(function (n) {
            e.appendGoogleButton(t, function () {
              n();
            });
          })), n && (i.applePay = new Promise(function (t) {
            e.appendAppleButton(n, function () {
              t();
            });
          })), r && (i.paypal = new Promise(function (t) {
            e.appendPaypalButton(r, function () {
              t();
            });
          })), i;
        }
      }, {
        key: "appendGoogleButton",
        value: function (t, n) {
          var r = this,
            i = this.configuration.clientSide.google;
          t && this.paymentButtonsView.canAppend(i) && e.canAppendGooglePay(t) ? (this.googlePay = new WC(t, e.googleButtonCss, {
            beforeMount: function () {},
            mounted: function () {
              r.messageBus.sendPublicMessage({
                type: bP.Mounted,
                entity: eT.GooglePay
              }), r.paymentButtonsView.show(), r.tracking.googleButtonMounted(), n();
            },
            mountFailed: function () {
              n();
            },
            pageOpened: function () {
              var e;
              null === (e = r.interactionsNotifier) || void 0 === e || e.processDsrpClick("googlePay"), r.tracking.googleButtonPageOpened();
            },
            pageClosed: function () {
              return r.tracking.googleButtonPageClosed();
            },
            pay: function (e) {
              var t;
              r.messageBus.sendPrivateMessage({
                type: bP.ProviderToken,
                value: e,
                dsrp: VC.Google
              }, null === (t = r.iframe) || void 0 === t ? void 0 : t.getWindow()), r.tracking.googleButtonPageSubmitted();
            }
          }, this.logger), this.googlePay.init(), this.googlePay.element.then(function (e) {
            r.isDestroyed || r.paymentButtonsView.append(e, i);
          }).catch(function (e) {
            n(), r.logger.debug(e);
          })) : n();
        }
      }, {
        key: "appendAppleButton",
        value: function (t, n) {
          var r = this,
            i = this.configuration.clientSide.apple;
          t && this.paymentButtonsView.canAppend(i) && e.canAppendApplePay(t) && $C.isPossibleToMakePayments() ? (this.applePay = new $C(t, "Seller", {
            beforeMount: function () {},
            mounted: function () {
              r.messageBus.sendPublicMessage({
                type: bP.Mounted,
                entity: eT.ApplePay
              }), r.paymentButtonsView.show(), r.tracking.appleButtonMounted(), n();
            },
            pageOpened: function () {
              return r.tracking.appleButtonPageOpened();
            },
            pageClosed: function () {
              return r.tracking.appleButtonPageClosed();
            },
            click: function () {
              var e;
              return null === (e = r.interactionsNotifier) || void 0 === e ? void 0 : e.processDsrpClick("applePay");
            },
            pay: function (e) {
              var t;
              r.messageBus.sendPrivateMessage({
                type: bP.ProviderToken,
                value: JSON.stringify(e),
                dsrp: VC.Apple
              }, null === (t = r.iframe) || void 0 === t ? void 0 : t.getWindow()), r.messageBus.sendPublicMessage({
                type: bP.ApplePayPaymentAuthorized,
                paymentMethod: e.paymentMethod
              }), r.tracking.appleButtonSubmitted();
            }
          }, function () {
            var e = l(s().mark(function e(t) {
              var n;
              return s().wrap(function (e) {
                for (;;) switch (e.prev = e.next) {
                  case 0:
                    return n = new QE(a(a({}, t), {}, {
                      headers: a(a({}, t.headers || {}), {}, {
                        Authorization: "Bearer ".concat(r.token),
                        "X-Release": r.release
                      })
                    }), {
                      times: 3,
                      time: 1e3,
                      whenOnline: !1
                    }), e.next = 3, n.execute();
                  case 3:
                    return e.abrupt("return", e.sent);
                  case 4:
                  case "end":
                    return e.stop();
                }
              }, e);
            }));
            return function (t) {
              return e.apply(this, arguments);
            };
          }()), this.applePay.init(), this.applePay.element.then(function (e) {
            r.isDestroyed || r.paymentButtonsView.append(e, i);
          }).catch(function () {
            return n();
          })) : n();
        }
      }, {
        key: "appendPaypalButton",
        value: function (t, n) {
          var r = this,
            i = this.configuration.clientSide.paypal;
          if (t && this.paymentButtonsView.canAppend(i) && e.canAppendPaypal(t)) {
            var o = this.tracking.paypalButtonMountTime();
            this.paypal = new QC(t, {
              onClick: function () {
                var e = l(s().mark(function e(t) {
                  var n;
                  return s().wrap(function (e) {
                    for (;;) switch (e.prev = e.next) {
                      case 0:
                        t && (null === (n = r.interactionsNotifier) || void 0 === n || n.processApmButtonClick("paypal"));
                      case 1:
                      case "end":
                        return e.stop();
                    }
                  }, e);
                }));
                return function (t) {
                  return e.apply(this, arguments);
                };
              }(),
              onCreateOrder: function () {
                var e = l(s().mark(function e() {
                  return s().wrap(function (e) {
                    for (;;) switch (e.prev = e.next) {
                      case 0:
                        return e.abrupt("return", new Promise(function (e, t) {
                          var n;
                          r.messageBus.subscribeForPrivate(function n(i) {
                            if (i.type === DP.PaypalOrderToken) {
                              var o;
                              if (tT(i)) e({
                                token: i.token
                              });else if (t(i.error), r.logger.error(i.error), null !== (o = i.error) && void 0 !== o && o.message.includes("is already in processing")) {
                                console.error("%cWarning! The PayPal button on the Payment Form cannot be used because a PayPal button has already been initialized via host-to-host with the same order ID.\n                      \n%cIf you are already using an existing PayPal host-to-host button, you should disable it so that orders are created and processed automatically by the payment form itself.\n                      \nSee more in the Payment Form documentation, section 'PayPal Button: Display Button.'", "font-weight: bold", "font-weight: normal");
                              }
                              r.messageBus.unsubscribe(n);
                            }
                          }), r.messageBus.sendPrivateMessage({
                            type: bP.PaypalCreateOrder
                          }, null === (n = r.iframe) || void 0 === n ? void 0 : n.getWindow());
                        }));
                      case 1:
                      case "end":
                        return e.stop();
                    }
                  }, e);
                }));
                return function () {
                  return e.apply(this, arguments);
                };
              }(),
              onStartProcessing: function () {
                var e = l(s().mark(function e(t) {
                  return s().wrap(function (e) {
                    for (;;) switch (e.prev = e.next) {
                      case 0:
                        t && r.messageBus.sendPublicMessage({
                          type: zP.Submit,
                          entity: eT.Paypal
                        });
                      case 1:
                      case "end":
                        return e.stop();
                    }
                  }, e);
                }));
                return function (t) {
                  return e.apply(this, arguments);
                };
              }(),
              onInit: function (e) {
                r.paymentButtonsView.show(), e && r.messageBus.sendPublicMessage({
                  type: bP.Mounted,
                  entity: eT.Paypal
                }), o(), n();
              },
              onOrderProcessed: function () {
                var e;
                r.messageBus.sendPrivateMessage({
                  type: bP.PaypalOrderProcessed
                }, null === (e = r.iframe) || void 0 === e ? void 0 : e.getWindow()), r.setIsDisabled(!0);
              },
              onError: function (e) {
                r.logger.error(e);
              }
            }), this.paypal.init(), this.paypal.element.then(function () {
              var e = l(s().mark(function e(t) {
                var o;
                return s().wrap(function (e) {
                  for (;;) switch (e.prev = e.next) {
                    case 0:
                      if (!r.isDestroyed) {
                        e.next = 2;
                        break;
                      }
                      return e.abrupt("return");
                    case 2:
                      return r.paymentButtonsView.append(t, a(a({}, i), {}, {
                        fullWidth: !0
                      })), e.prev = 3, e.next = 6, null === (o = r.paypal) || void 0 === o ? void 0 : o.appendButton();
                    case 6:
                      e.next = 13;
                      break;
                    case 8:
                      e.prev = 8, e.t0 = e.catch(3), r.paymentButtonsView.remove(t), r.logger.error(e.t0), n();
                    case 13:
                    case "end":
                      return e.stop();
                  }
                }, e, null, [[3, 8]]);
              }));
              return function (t) {
                return e.apply(this, arguments);
              };
            }()).catch(function (e) {
              n(), r.logger.debug(e);
            });
          } else n();
        }
      }, {
        key: "clear",
        value: function () {
          var e;
          null === (e = this.applePay) || void 0 === e || e.destroy(), this.googlePay = null, this.applePay = null, this.paypal = null, this.paymentButtonsView.destroy();
        }
      }], [{
        key: "prefetch",
        value: function () {
          WC.prefetch();
        }
      }, {
        key: "canAppendGooglePay",
        value: function (e) {
          return !(!e || !e.merchantId);
        }
      }, {
        key: "canAppendApplePay",
        value: function (e) {
          return !(!e || !e.createSessionUrl);
        }
      }, {
        key: "canAppendPaypal",
        value: function (e) {
          return !!(e && e.credentials && e.credentials.clientId && e.baseApiPath && e.antifraud);
        }
      }]);
    }();
  nT.googleButtonCss = "\n        button.gpay-card-info-container {\n          min-width: 160px\n        }\n      ";
  var rT,
    iT = window.innerWidth <= 500,
    oT = {
      position: "relative",
      backgroundColor: "white",
      height: iT ? "100%" : "600px",
      width: iT ? "100%" : "500px",
      maxWidth: "100vw",
      maxHeight: "100vv",
      borderRadius: iT ? "0px" : "12px"
    },
    aT = {
      display: "none",
      transition: "opacity 0.2s ease-in",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      zIndex: "2147483647",
      height: "100vh",
      width: "100vw",
      position: "fixed",
      opacity: "0",
      top: "0",
      left: "0",
      backgroundColor: "rgba(0, 0, 0, 0.8)"
    },
    sT = a(a({}, oT), {}, {
      height: "auto",
      width: "auto",
      minHeight: "168px",
      minWidth: "368px"
    }),
    uT = {
      paddingTop: "24px",
      paddingBottom: "8px",
      margin: "0 auto",
      width: "48px"
    },
    cT = {
      position: "absolute",
      top: "16px",
      right: "16px",
      cursor: "pointer"
    },
    lT = {
      fontFamily: "Arial",
      fontStyle: "normal",
      fontWeight: "400",
      fontSize: "14px",
      lineHeight: "24px",
      textAlign: "center",
      maxWidth: "264px",
      boxSizing: "border-box",
      padding: "0 24px 40px",
      margin: "0 auto",
      color: "#000000"
    },
    fT = {
      height: "100%",
      width: "100%",
      borderRadius: "inherit",
      border: "none"
    },
    hT = function () {
      return d(function e(t) {
        f(this, e), this.uuid = t, this.iframe = null, this.iframeId = "verify-iframe-modal-".concat(this.uuid()), this.modal = this.createThreeDSModal();
      }, [{
        key: "open",
        value: function (e) {
          var t = this,
            n = e.url,
            r = e.onSuccess;
          this.iframe && (this.iframe.src = n), r(), this.modal.style.display = "flex", setTimeout(function () {
            t.modal.style.opacity = "1";
          }, 40);
        }
      }, {
        key: "close",
        value: function () {
          var e = this;
          this.modal && (setTimeout(function () {
            e.modal.style.opacity = "0";
          }, 40), setTimeout(function () {
            try {
              var t;
              null !== (t = document) && void 0 !== t && null !== (t = t.body) && void 0 !== t && t.contains(e.modal) && document.body.removeChild(e.modal);
            } catch (n) {}
          }, 300));
        }
      }, {
        key: "getWindow",
        value: function () {
          return window.frames[this.iframeId];
        }
      }, {
        key: "createThreeDSModal",
        value: function () {
          var e = this.create3DSIframe(),
            t = document.createElement("div");
          Object.assign(t.style, oT), t.appendChild(e);
          var n = document.createElement("div");
          return n.appendChild(t), Object.assign(n.style, aT), document.body.appendChild(n), n;
        }
      }, {
        key: "create3DSIframe",
        value: function () {
          var e = document.createElement("iframe");
          return e.setAttribute("test-id", "verify-iframe-modal-test-id"), e.id = this.iframeId, e.name = this.iframeId, Object.assign(e.style, fT), this.iframe = e, e;
        }
      }]);
    }(),
    dT = function () {
      function e(t) {
        var n = this;
        f(this, e), this.message = t, this.messageBox = null, this.modal = this.createThreeDSModal(), this.close = function () {
          n.modal && (setTimeout(function () {
            n.modal.style.opacity = "0";
          }, 40), setTimeout(function () {
            var e;
            return null === (e = document) || void 0 === e ? void 0 : e.body.removeChild(n.modal);
          }, 300));
        };
      }
      return d(e, [{
        key: "open",
        value: function () {
          var e = l(s().mark(function e(t) {
            var n,
              r,
              i,
              o = this;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  return n = t.url, r = t.onSuccess, i = t.onFail, e.next = 3, this.openNewTab(n);
                case 3:
                  if (e.sent) {
                    e.next = 7;
                    break;
                  }
                  return i(), e.abrupt("return");
                case 7:
                  this.messageBox && (this.messageBox.innerText = this.message || ""), r(), this.modal.style.display = "flex", setTimeout(function () {
                    o.modal.style.opacity = "1";
                  }, 40);
                case 11:
                case "end":
                  return e.stop();
              }
            }, e, this);
          }));
          return function (t) {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "getWindow",
        value: function () {}
      }, {
        key: "openNewTab",
        value: function (e) {
          var t = window.open(e, "_blank");
          return Promise.resolve(!(null == t || !t.opener));
        }
      }, {
        key: "createThreeDSModal",
        value: function () {
          var e = this.createIcon(),
            t = this.createMessageBox(),
            n = this.createCross();
          this.messageBox = t;
          var r = document.createElement("div");
          Object.assign(r.style, sT);
          var i = document.createElement("div");
          return Object.assign(i.style, aT), r.appendChild(e), r.appendChild(t), r.appendChild(n), i.appendChild(r), document.body.appendChild(i), i;
        }
      }, {
        key: "createIcon",
        value: function () {
          var t = document.createElement("div");
          return Object.assign(t.style, uT), t.innerHTML = e.iconSvg, t;
        }
      }, {
        key: "createCross",
        value: function () {
          var t = this,
            n = document.createElement("div");
          return Object.assign(n.style, cT), n.innerHTML = e.crossSvg, n.addEventListener("click", function () {
            return t.close();
          }), n;
        }
      }, {
        key: "createMessageBox",
        value: function () {
          var t = document.createElement("div");
          return Object.assign(t.style, lT), t.innerHTML = e.iconSvg, t;
        }
      }]);
    }();
  (rT = dT).iconSvg = '\n    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">\n      <rect x="15" y="7" width="30" height="22" rx="2" stroke="#2771FF" stroke-width="2"/>\n      <path opacity="0.4" d="M14 18H5C3.34315 18 2 19.3431 2 21V39C2 40.6569 3.34315 42 5 42H31C32.6569 42 34 40.6569 34 39V30H32V39C32 39.5523 31.5523 40 31 40H5C4.44772 40 4 39.5523 4 39V21C4 20.4477 4.44772 20 5 20H14V18Z" fill="#2771FF"/>\n    </svg>\n  ', rT.crossSvg = '\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">\n      <path fill-rule="evenodd" clip-rule="evenodd" d="M10.9394 12L4.46973 5.53033L5.53039 4.46967L12.0001 10.9393L18.4697 4.46967L19.5304 5.53033L13.0607 12L19.5304 18.4697L18.4697 19.5303L12.0001 13.0607L5.53039 19.5303L4.46973 18.4697L10.9394 12Z" fill="#BEBEBE"/>\n    </svg>\n  ';
  var pT = function () {
      return d(function e(t, n, r, i, o) {
        f(this, e), this.logger = t, this.merchantLogger = n, this.messageBus = r, this.tracking = i, this.uuid = o, this.initConfig = null, this.resignConfig = null, this.initialized = !1, this.iframe = null, this.interactionsNotifier = null, this.paymentsButtons = null, this.threeDSFlow = null, this.intent = null, this.previousIntent = null, nT.prefetch();
      }, [{
        key: "flush",
        value: function () {
          var e, t, n;
          null === (e = this.threeDSFlow) || void 0 === e || e.close(), null === (t = this.iframe) || void 0 === t || t.destroy(), null === (n = this.paymentsButtons) || void 0 === n || n.destroy(), this.tracking.clear(), this.threeDSFlow = null, this.iframe = null, this.paymentsButtons = null, this.initConfig = null, this.resignConfig = null, this.previousIntent = this.intent, this.intent = null;
        }
      }, {
        key: "choose3DSFlowScenario",
        value: function (e, t, n) {
          var r = this;
          e === ax.Modal ? this.threeDSFlow = new hT(this.uuid) : e === ax.Tab ? this.threeDSFlow = new dT(n || "") : this.logger.error(new Error("Unsupported verify open flow"), {
            url: t
          }), this.threeDSFlow && this.threeDSFlow.open({
            url: t,
            onFail: function () {
              var t;
              return r.messageBus.sendPrivateMessage({
                type: bP.PerformVerifyResult,
                verifyType: e,
                isSuccess: !1
              }, null === (t = r.iframe) || void 0 === t ? void 0 : t.getWindow());
            },
            onSuccess: function () {
              var t;
              return r.messageBus.sendPrivateMessage({
                type: bP.PerformVerifyResult,
                verifyType: e,
                isSuccess: !0
              }, null === (t = r.iframe) || void 0 === t ? void 0 : t.getWindow());
            }
          });
        }
      }, {
        key: "resize",
        value: function (e) {
          var t, n, r, i, o;
          null === (t = this.iframe) || void 0 === t || t.resize(e), null === (n = this.paymentsButtons) || void 0 === n || n.resize();
          var a = parseInt(e.height.toString() || (null === (r = this.iframe) || void 0 === r ? void 0 : r.height) || "0");
          return {
            width: parseInt((null === (i = e.width) || void 0 === i ? void 0 : i.toString()) || (null === (o = this.iframe) || void 0 === o ? void 0 : o.width) || "0"),
            height: a,
            visible: !!this.iframe && !this.iframe.isHidden
          };
        }
      }, {
        key: "sendErrorToMerchant",
        value: function (e) {
          var t;
          this.merchantLogger.error(e), function (e) {
            return e instanceof Error && !!e.details;
          }(e) && (t = e.details);
          try {
            this.messageBus.sendPublicMessage({
              type: zP.Error,
              value: {
                name: e.name,
                message: e.message,
                stack: e.stack
              },
              details: t
            });
          } catch (DO) {
            this.logger.error(new QP("Unable to send error to merchant"), DO);
          }
        }
      }, {
        key: "sendTokenToForm",
        value: function (e) {
          var t,
            n,
            r,
            i = (null === (t = this.intent) || void 0 === t ? void 0 : t.id) === e,
            o = !!this.intent;
          this.messageBus.sendPrivateMessage({
            type: bP.TokenResponse,
            token: this.intent && i ? this.intent.token : ""
          }, null === (n = this.threeDSFlow) || void 0 === n ? void 0 : n.getWindow()), this.messageBus.sendPrivateMessage({
            type: bP.TokenResponse,
            token: this.intent && i ? this.intent.token : ""
          }, null === (r = this.iframe) || void 0 === r ? void 0 : r.getWindow()), o || this.logger.error(new ux("no intent")), i || this.logger.error(new ux("foreign intent"));
        }
      }, {
        key: "getLastKnownIntentTracking",
        value: function () {
          var e = this.intent || this.previousIntent;
          return null == e ? void 0 : e.tracking;
        }
      }]);
    }(),
    gT = function () {
      return d(function e() {
        f(this, e);
      }, null, [{
        key: "resolveNewPrice",
        value: function (e) {
          return e.trialPrice ? e.trialPrice : e.discountPrice;
        }
      }]);
    }(),
    vT = function (e) {
      function n(e) {
        var r;
        f(this, n);
        var i = "string" == typeof e ? e : JSON.stringify(e);
        return (r = t(this, n, ["Unable to apply coupon: ".concat(i)])).name = "ApplyCouponError", "string" != typeof e && (r.details = e), r;
      }
      return g(n, e), d(n);
    }(m(Error)),
    yT = d(function e() {
      var t = this;
      f(this, e), this.onSuccess = function () {}, this.onFail = function () {}, this.isCompleted = !1, this.result = new Promise(function (e, n) {
        t.onSuccess = e, t.onFail = n;
      }), this.result.catch(function () {}).then(function () {
        t.isCompleted = !0;
      });
    }),
    mT = function (e) {
      function n(e, r, i, o) {
        var a;
        return f(this, n), (a = t(this, n)).couponCode = e, a.context = r, a.messageBus = i, a.logger = o, a.trace = null, a;
      }
      return g(n, e), d(n, [{
        key: "handleSuccess",
        value: function (e) {
          var t,
            n = this.context.paymentsButtons,
            r = gT.resolveNewPrice(e);
          null == n || n.update({
            price: {
              amount: r.amount,
              currency: r.currency
            }
          }), null == n || n.setIsDisabled(!1), this.onSuccess(e), null === (t = this.trace) || void 0 === t || t.finish();
        }
      }, {
        key: "handleFail",
        value: function (e, t) {
          var n,
            r = this.context.paymentsButtons;
          null == r || r.setIsDisabled(!1), this.onFail(e), null === (n = this.trace) || void 0 === n || n.finish(t);
        }
      }, {
        key: "applyCouponFinished",
        value: function () {
          var e = this;
          return new Promise(function (t) {
            e.messageBus.subscribeForPrivate(function n(r) {
              r.type === DP.CouponApplied && (e.messageBus.unsubscribe(n), t(r));
            });
          });
        }
      }, {
        key: "validate",
        value: function () {
          var e;
          return null !== (e = this.context.iframe) && void 0 !== e && e.isPresentInDOM() ? null : [Pk.Cancelled, new vT("Payment form iframe not found")];
        }
      }, {
        key: "execute",
        value: function () {
          var e = l(s().mark(function e() {
            var t,
              n,
              r,
              i,
              o,
              a,
              u = this;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  if (!this.context.resignConfig) {
                    e.next = 3;
                    break;
                  }
                  return this.handleFail(new vT("Resign intents does not support coupons"), Pk.InvalidArgument), e.abrupt("return");
                case 3:
                  return this.trace = this.logger.trace("ApplyCoupon"), this.logLongExecution(), n = this.context.paymentsButtons, null !== (r = this.validate()) && (i = w(r, 2), o = i[0], a = i[1], this.handleFail(a, o)), null == n || n.setIsDisabled(!0), this.messageBus.sendPrivateMessage({
                    type: bP.ApplyCoupon,
                    couponCode: this.couponCode
                  }, null === (t = this.context.iframe) || void 0 === t ? void 0 : t.getWindow()), e.abrupt("return", Promise.race([this.context.iframe.unmounted().then(function () {
                    u.isCompleted || u.handleFail(new vT("Payment form iframe was removed from DOM before update ended"), Pk.Cancelled);
                  }), this.applyCouponFinished().then(function (e) {
                    u.isCompleted || (e.error ? u.handleFail(new vT(e.error), Pk.InvalidArgument) : u.handleSuccess({
                      productPrice: e.productPrice,
                      discountPrice: e.discountPrice,
                      trialPrice: e.trialPrice
                    }));
                  })]));
                case 11:
                case "end":
                  return e.stop();
              }
            }, e, this);
          }));
          return function () {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "logLongExecution",
        value: function () {
          var e = this,
            t = this.trace;
          setTimeout(function () {
            e.isCompleted || (e.logger.withinContext(t, function () {
              e.logger.error(new vT("Update took more than 90 seconds, giving up"));
            }), t.finish(Pk.InternalError), e.onFail(new vT("Internal error during update")));
          }, 9e4);
        }
      }]);
    }(yT),
    bT = function (e) {
      return e.Default = "default", e.Continue = "continue", e;
    }(bT || {}),
    wT = function (e) {
      return e.Default = "default", e.Card = "card", e.Inline = "inline", e.Flat = "flat", e;
    }(wT || {}),
    kT = function (e) {
      return e.Payment = "payment", e.Resign = "resign", e;
    }(kT || {});
  function PT(e) {
    return new Promise(function (t) {
      return setTimeout(t, e);
    });
  }
  function xT(e) {
    window.requestAnimationFrame ? window.requestAnimationFrame(e) : setTimeout(e, 0);
  }
  var ST = function (e) {
      function n() {
        var e;
        return f(this, n), (e = t(this, n, arguments)).name = "ConnectionError", e.message = "It seems user currently experiencing some problems with connection", e;
      }
      return g(n, e), d(n);
    }(m(Error)),
    CT = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, [e])).name = "FormInitializationDtoError", r;
      }
      return g(n, e), d(n);
    }(m(Error)),
    ET = ze,
    TT = ut,
    OT = ne,
    IT = Nr,
    AT = TypeError,
    LT = "Reduce of empty array with no initial value",
    jT = function (e) {
      return function (t, n, r, i) {
        var o = TT(t),
          a = OT(o),
          s = IT(o);
        if (ET(n), 0 === s && r < 2) throw new AT(LT);
        var u = e ? s - 1 : 0,
          c = e ? -1 : 1;
        if (r < 2) for (;;) {
          if (u in a) {
            i = a[u], u += c;
            break;
          }
          if (u += c, e ? u < 0 : s <= u) throw new AT(LT);
        }
        for (; e ? u >= 0 : s > u; u += c) u in a && (i = n(i, a[u], u, o));
        return i;
      };
    },
    RT = {
      left: jT(!1),
      right: jT(!0)
    }.left;
  Si({
    target: "Array",
    proto: !0,
    forced: !jo && Ce > 79 && Ce < 83 || !Hw("reduce")
  }, {
    reduce: function (e) {
      var t = arguments.length;
      return RT(this, e, t, t > 1 ? arguments[1] : void 0);
    }
  });
  var BT = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, [e])).name = "PaymentButtonsViewError", r;
      }
      return g(n, e), d(n);
    }(m(Error)),
    _T = "payment-buttons",
    NT = "payment-buttons-column",
    FT = ["form_body", "card_number", "expiry_date", "card_cvv", "card_holder", "zip_code", "card_cpf", "card_dni", "card_pin", "card_curp", "email", "submit_button", "header", "form_title", "two-columns", "card_view", "body_errors", "card_brands", "secure_info", "input_group", "additional_field", "resign-form", "resign-form-content", "resign-card-preview", "resign-card-brand-icon", "resign-unknown-card-icon", "resign-card-preview-content", "resign-card-card-brand-name", "resign-card-ending-in-text", "resign-card-last-four", "resign-input-group", "resign-input-block", "resign-label", "resign-cvv", "resign-dotted-placeholder", "resign-tooltip-icon", "resign-tooltip", "resign-submit-button"],
    MT = {
      opacity: 0,
      position: "absolute",
      zIndex: "-99999999"
    },
    UT = {
      opacity: 1,
      position: "static",
      zIndex: "initial"
    },
    DT = function () {
      return d(function e(t, n, r) {
        f(this, e), this.iframe = t, this.logger = n, this.merchantLogger = r, this.isShown = !1, this.buttons = [];
      }, [{
        key: "canAppend",
        value: function (e) {
          return null != e && e.containerId && !document.getElementById(e.containerId) && this.merchantLogger.warning(new BT("Container for payment button with id: ".concat(e.containerId, " does not exist"))), !(null != e && e.hasOwnProperty("enabled") && (null == e || !e.enabled));
        }
      }, {
        key: "append",
        value: function (e, t) {
          var n;
          this.buttons.push([t, e]), null === (n = this.getContainer(t)) || void 0 === n || n.appendChild(e);
        }
      }, {
        key: "remove",
        value: function (e) {
          var t = e.parentElement;
          e.remove(), t && !t.children.length && t.remove();
        }
      }, {
        key: "destroy",
        value: function () {
          var e,
            t,
            n = this;
          this.buttons.forEach(function (e) {
            var t = w(e, 1)[0],
              r = n.getCustomContainer(t);
            r && (r.innerHTML = "");
          }), null === (e = this.getInlineContainer()) || void 0 === e || e.remove(), null === (t = this.getColumnContainer()) || void 0 === t || t.remove(), this.buttons = [];
        }
      }, {
        key: "show",
        value: function () {
          this.isShown = !0, this.getAllContainers().forEach(function (e) {
            Object.assign(e.style, UT);
          });
        }
      }, {
        key: "resize",
        value: function () {
          var e = this.getInlineContainer(),
            t = this.getColumnContainer();
          e && (e.style.width = this.iframe.width), t && (t.style.width = this.iframe.width);
        }
      }, {
        key: "setIsDisabled",
        value: function (e) {
          this.buttons.forEach(function (t) {
            var n = w(t, 2);
            n[0];
            var r = n[1];
            r && (r.disabled = e, r.style.opacity = e ? "0.8" : "1", r.style.pointerEvents = e ? "none" : "initial");
          });
        }
      }, {
        key: "getAllContainers",
        value: function () {
          var e = this,
            t = this.buttons.reduce(function (t, n) {
              var r = w(n, 1)[0],
                i = e.getContainer(r);
              return i && t.push(i), t;
            }, []),
            n = this.getInlineContainer(),
            r = this.getColumnContainer();
          return [].concat(k(t), k(n ? [n] : []), k(r ? [r] : []));
        }
      }, {
        key: "getContainer",
        value: function (e) {
          return this.getCustomContainer(e) || this.getOrCreateDefaultContainer(e);
        }
      }, {
        key: "getCustomContainer",
        value: function (e) {
          if (null != e && e.containerId) return document.getElementById(e.containerId);
        }
      }, {
        key: "getOrCreateDefaultContainer",
        value: function (e) {
          var t = this.getInlineContainer() || this.createInlineContainer(),
            n = this.getColumnContainer() || this.createColumnContainer(),
            r = document.getElementById(this.iframe.containerId);
          if (r) {
            if (null != e && e.fullWidth) return n ? (this.insertColumnContainer(n, r), n) : void this.logger.error(new BT("Column container does not exist"));
            if (t) return this.insertInlineContainer(t, r), t;
            this.logger.error(new BT("Container does not exist"));
          } else this.merchantLogger.error(GP.DoesNotExist(this.iframe.containerId));
        }
      }, {
        key: "getInlineContainer",
        value: function () {
          return document.getElementById(_T);
        }
      }, {
        key: "getColumnContainer",
        value: function () {
          return document.getElementById(NT);
        }
      }, {
        key: "insertInlineContainer",
        value: function (e, t) {
          if (!this.getInlineContainer()) {
            var n = this.getColumnContainer();
            n ? n.before(e) : t.prepend(e);
          }
        }
      }, {
        key: "insertColumnContainer",
        value: function (e, t) {
          if (!this.getColumnContainer()) {
            var n = this.getInlineContainer();
            n ? n.after(e) : t.prepend(e);
          }
        }
      }, {
        key: "createInlineContainer",
        value: function () {
          var e = document.createElement("div");
          return e.id = _T, e.className = "".concat(_T), Object.assign(e.style, a({
            width: this.iframe.width,
            padding: "0",
            marginBottom: "0.5em",
            display: "grid",
            gap: "0.5em",
            height: "3.3em",
            boxSizing: "border-box",
            gridTemplateColumns: "repeat(auto-fit, minmax(50px, 1fr))",
            gridTemplateRows: "3.3em"
          }, this.isShown ? UT : MT)), e;
        }
      }, {
        key: "createColumnContainer",
        value: function () {
          var e = document.createElement("div");
          return e.id = NT, e.className = "".concat(NT), Object.assign(e.style, a({
            width: this.iframe.width,
            padding: "0",
            display: "grid",
            marginBottom: "0.5em",
            gap: "0.5em",
            boxSizing: "border-box",
            gridTemplateColumns: "minmax(50px, 1fr)",
            gridAutoRows: "3.3em"
          }, this.isShown ? UT : MT)), e;
        }
      }]);
    }(),
    zT = function (e) {
      return e.Input = "input", e.Button = "button", e;
    }(zT || {}),
    VT = function (e) {
      return e.Click = "click", e.Focus = "focus", e.Blur = "blur", e.Change = "change", e.EnterKeyDown = "enterKeyDown", e;
    }(VT || {}),
    qT = function (e) {
      return e.CardNumber = "cardNumber", e.CardCvv = "cardCvv", e.CardExpiryDate = "cardExpiryDate", e.CardHolder = "cardHolder", e.Zip = "zip", e.Email = "email", e.BrazilCustomerPhone = "brazilCustomerPhone", e.BrazilZip = "brazilZip", e;
    }(qT || {}),
    $T = function (e) {
      return e.ResignCvv = "resignCvv", e;
    }($T || {}),
    GT = function () {
      return d(function e(t, n) {
        switch (f(this, e), this.messageBus = t, n) {
          case "cardForm":
            this.state = {
              cardForm: {
                fields: p(p(p({}, qT.CardNumber, {
                  isValid: !1,
                  isTouched: !1
                }), qT.CardCvv, {
                  isValid: !1,
                  isTouched: !1
                }), qT.CardExpiryDate, {
                  isValid: !1,
                  isTouched: !1
                }),
                isTouched: !1,
                isValid: !1
              }
            };
            break;
          case "resignForm":
            this.state = {
              resignForm: {
                fields: p({}, $T.ResignCvv, {
                  isValid: !1,
                  isTouched: !1
                }),
                isTouched: !1,
                isValid: !1
              }
            };
        }
      }, [{
        key: "processFormMessage",
        value: function (e) {
          this.state = e, this.messageBus.sendPublicMessage(a(a({}, JSON.parse(JSON.stringify(e))), {}, {
            type: bP.Interaction
          }));
        }
      }, {
        key: "processDsrpClick",
        value: function (e) {
          this.messageBus.sendPublicMessage(a(a({}, JSON.parse(JSON.stringify(this.state))), {}, {
            type: bP.Interaction,
            target: {
              type: zT.Button,
              name: e,
              interaction: VT.Click
            }
          }));
        }
      }, {
        key: "processApmButtonClick",
        value: function (e) {
          this.messageBus.sendPublicMessage(a(a({}, JSON.parse(JSON.stringify(this.state))), {}, {
            type: bP.Interaction,
            target: {
              type: zT.Button,
              name: e,
              interaction: VT.Click
            }
          }));
        }
      }]);
    }(),
    HT = function (e) {
      return e.Default = "default", e.React = "react", e.Angular = "angular", e.Vue = "vue", e;
    }(HT || {}),
    WT = function (e) {
      return e.FormBody = ".form_body", e.TwoColumns = ".two-columns", e.CardView = ".card_view", e;
    }(WT || {});
  function JT(e) {
    for (var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : "", n = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : {}, r = 0, i = Object.keys(e); r < i.length; r++) {
      var o = i[r],
        a = e[o];
      if ("object" == typeof a && !Array.isArray(a) && a) {
        var s = void 0;
        s = o.includes(":") ? "" : FT.includes(o) ? "." : " ", JT(a, t + "".concat(s).concat(o), n);
      } else {
        var u = [":", WT.TwoColumns, WT.CardView],
          c = t === WT.FormBody,
          l = t.includes(WT.FormBody) && u.some(function (e) {
            return t.includes(e);
          }),
          f = !t.includes(WT.FormBody);
        (l || c || f) && (n["".concat(t)] ? n["".concat(t)][o] = a : n["".concat(t)] = p({}, o, a));
      }
    }
    return n;
  }
  function ZT(e) {
    return e ? "string" == typeof e ? {} : function (e) {
      var t = JSON.stringify(e),
        n = {
          card_cpf: "brazil_cpf",
          card_dni: "argentina_dni",
          card_curp: "mexico_curp"
        };
      return Object.keys(n).forEach(function (e) {
        var r = new RegExp(e, "g");
        t = t.replace(r, n[e]);
      }), JSON.parse(t);
    }(JT(Object.keys(e).filter(function (e) {
      return FT.includes(e);
    }).reduce(function (t, n) {
      return t[n] = e[n], t;
    }, {}))) : {};
  }
  var XT = function () {
      return d(function e(t, n, r, i) {
        var o;
        f(this, e), this.config = t, this.branding = n, this.sdkVersion = r, this.logger = i, this.payload = {
          styles: null
        }, this.initType = null !== (o = n.getSdkInitType()) && void 0 !== o ? o : HT.Default, this.addMerchantStyles(t.styles), this.verifyInitType(), this.addMetadata();
      }, [{
        key: "toJSON",
        value: function (e) {
          return a({
            type: bP.FormInitialization,
            paymentType: kT.Payment,
            originalConfig: this.config,
            integrity: e
          }, this.payload);
        }
      }, {
        key: "toApiCall",
        value: function () {
          return a(a({}, this.config.merchantData), {}, {
            sdkVersion: this.sdkVersion,
            meta: this.payload.meta
          });
        }
      }, {
        key: "isIframeHidden",
        value: function () {
          var e;
          return !1 === (null === (e = this.config.formParams) || void 0 === e ? void 0 : e.enabled);
        }
      }, {
        key: "styles",
        get: function () {
          return this.payload.styles;
        }
      }, {
        key: "addMerchantStyles",
        value: function (e) {
          if (e) {
            var t = ZT(e);
            Object.keys(t).length && (this.payload.styles = t);
          }
        }
      }, {
        key: "addMetadata",
        value: function () {
          var e,
            t = this.branding.getIsBrandedLogoParameterName();
          this.payload.meta = {
            isBrandLogoDefined: !!this.config.formParams && void 0 !== this.config.formParams[t],
            isFrameworkSdkUsed: !!this.branding.getSdkInitType(),
            cdn: this.branding.getCdnList(),
            customContainerId: (null === (e = this.config) || void 0 === e || null === (e = e.iframeParams) || void 0 === e ? void 0 : e.containerId) || this.branding.getDefaultFormId()
          };
        }
      }, {
        key: "verifyInitType",
        value: function () {
          var e = this;
          Object.values(HT).some(function (t) {
            return t === e.initType;
          }) || (this.logger.error(new CT("Unrecognized init type ".concat(this.initType))), this.initType = HT.Default);
        }
      }]);
    }(),
    YT = function (e) {
      return e.VisaSecure = "visa-secure", e.MccIdCheck = "mcc-id-check", e.SSL = "ssl", e.PCIDss = "pci-dss", e.Norton = "norton", e.McAffee = "mc-affee", e;
    }(YT || {}),
    KT = function () {
      return d(function e(t) {
        f(this, e), this.schema = t;
      }, [{
        key: "validate",
        value: function (e) {
          var t = this,
            n = {},
            r = !0;
          return Object.keys(e).forEach(function (i) {
            var o = e[i],
              a = t.schema[i];
            if (!a) return !0;
            var s = a(o);
            s.isValid || (n[i] = s.reason, r = !1);
          }), r ? [!0] : [!1, n];
        }
      }], [{
        key: "string",
        value: function (e) {
          return "string" == typeof e ? {
            isValid: !0
          } : {
            isValid: !1,
            reason: "Value should be a string"
          };
        }
      }, {
        key: "boolean",
        value: function (e) {
          return "boolean" == typeof e ? {
            isValid: !0
          } : {
            isValid: !1,
            reason: "Value should be a boolean"
          };
        }
      }, {
        key: "oneOf",
        value: function (e) {
          return function (t) {
            return e.includes(t) ? {
              isValid: !0
            } : {
              isValid: !1,
              reason: "Value should be one of: '".concat(e.join("', '"), "'")
            };
          };
        }
      }, {
        key: "isArray",
        value: function (e) {
          return Array.isArray(e) ? {
            isValid: !0
          } : {
            isValid: !1,
            reason: "Value should be an array"
          };
        }
      }, {
        key: "isArrayOf",
        value: function (e) {
          return function (t) {
            return Array.isArray(t) ? t.every(function (t) {
              return e.includes(t);
            }) ? {
              isValid: !0
            } : {
              isValid: !1,
              reason: "Value should be an array of: '".concat(e.join("', '"), "'")
            } : {
              isValid: !1,
              reason: "Value should be an array"
            };
          };
        }
      }]);
    }(),
    QT = function (e) {
      function n() {
        f(this, n);
        var e = qC.reduce(function (e, t) {
          return e["".concat(t, "Label")] = KT.string, e["".concat(t, "Placeholder")] = KT.string, e;
        }, {});
        return t(this, n, [a({
          enabled: KT.boolean,
          autoFocus: KT.boolean,
          buttonType: KT.oneOf(Object.values(bT)),
          submitButtonText: KT.string,
          isCardHolderVisible: KT.boolean,
          hideCvvNumbers: KT.boolean,
          headerText: KT.string,
          titleText: KT.string,
          formTypeClass: KT.oneOf(Object.values(wT)),
          isSolidLogoVisible: KT.boolean,
          cardBrands: KT.isArrayOf(Object.values(zC)),
          secureBrands: KT.isArrayOf(Object.values(YT)),
          allowSubmit: KT.boolean,
          googleFontLink: KT.string,
          cardNumberLabel: KT.string,
          cardNumberPlaceholder: KT.string,
          cardCvvLabel: KT.string,
          cardCvvPlaceholder: KT.string,
          cardExpiryDateLabel: KT.string,
          cardExpiryDatePlaceholder: KT.string,
          emailLabel: KT.string,
          emailPlaceholder: KT.string,
          zipCodeLabel: KT.string,
          zipCodePlaceholder: KT.string
        }, e)]);
      }
      return g(n, e), d(n);
    }(KT),
    eO = function (e) {
      function n() {
        f(this, n);
        var e = qC.reduce(function (e, t) {
          return e["".concat(t, "Label")] = KT.string, e["".concat(t, "Placeholder")] = KT.string, e;
        }, {});
        return t(this, n, [a({
          enabled: KT.oneOf([!0, !1, "true"]),
          autoFocus: KT.oneOf([!0, !1, "true"]),
          buttonType: KT.string,
          submitButtonText: KT.string,
          isCardHolderVisible: KT.oneOf([!0, !1, "true"]),
          hideCvvNumbers: KT.oneOf([!0, !1, "true"]),
          headerText: KT.string,
          titleText: KT.string,
          formTypeClass: KT.string,
          isSolidLogoVisible: KT.oneOf([!0, !1, "true", "false"]),
          cardBrands: KT.isArray,
          secureBrands: KT.isArray,
          allowSubmit: KT.oneOf([!0, !1, "true", "false"]),
          googleFontLink: KT.string,
          cardNumberLabel: KT.string,
          cardNumberPlaceholder: KT.string,
          cardCvvLabel: KT.string,
          cardCvvPlaceholder: KT.string,
          cardExpiryDateLabel: KT.string,
          cardExpiryDatePlaceholder: KT.string,
          emailLabel: KT.string,
          emailPlaceholder: KT.string,
          zipCodeLabel: KT.string,
          zipCodePlaceholder: KT.string
        }, e)]);
      }
      return g(n, e), d(n);
    }(KT),
    tO = function (e) {
      function n(e, r, i, o, a, s, u, c, l, h, d, p) {
        var g;
        return f(this, n), (g = t(this, n)).config = e, g.context = r, g.logger = i, g.api = o, g.tracking = a, g.branding = s, g.merchantLogger = u, g.messageBus = c, g.uuid = l, g.release = h, g.iframePool = d, g.locationService = p, g.readyMessageState = "Initial", g.paymentButtonsExist = !1, g.iframe = null, g.trace = null, g;
      }
      return g(n, e), d(n, [{
        key: "execute",
        value: function () {
          var e = l(s().mark(function e() {
            var t,
              n,
              r,
              i,
              o,
              a,
              u,
              c,
              f,
              h,
              d,
              p,
              g,
              v,
              y,
              m,
              b,
              k,
              P = this;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  if (this.context.initialized && this.context.flush(), this.context.initialized = !0, t = this.validate(), n = w(t, 2), r = n[0], i = n[1], r) {
                    e.next = 6;
                    break;
                  }
                  return this.onFail(i), e.abrupt("return");
                case 6:
                  return o = new XT(this.config, this.branding, this.release, this.logger), a = this.uuid(), this.trace = this.logger.trace("Initialization-v2"), this.logLongExecution(), this.context.initConfig = this.config, u = this.trace.addSpan("IframeLoading", "resource"), c = this.iframePool.getIframe(), this.context.iframe = c, e.next = 16, this.mountIframe(c, a);
                case 16:
                  if ("Mounted" === c.state) {
                    e.next = 20;
                    break;
                  }
                  return this.trace.finish(Pk.NotFound), this.onFail(new QP("Element with containerId: ".concat(null === (f = this.config.iframeParams) || void 0 === f ? void 0 : f.containerId, " is missing"))), e.abrupt("return");
                case 20:
                  return h = this.tracking.initTime(), this.iframe = c, c.onLoad(function () {
                    P.tracking.scriptLoadTime(), P.messageBus.sendPrivateMessage(o.toJSON(a), c.getWindow()), u.finish();
                  }), d = this.trace.addSpan("InitPaymentRequest", "http"), e.next = 26, this.api.init(o.toApiCall());
                case 26:
                  if (p = e.sent, g = p.result, v = p.retries, !(g instanceof Error)) {
                    e.next = 34;
                    break;
                  }
                  return this.context.sendErrorToMerchant(g), this.onFail(g), this.trace.finish(Pk.PermissionDenied), e.abrupt("return");
                case 34:
                  return this.tracking.initNetworkError(v), d.finish(), this.context.intent = g, g.tracking && this.tracking.init(g.tracking.trackSignature, g.tracking.trackId), c.setIntentMetadata(g.id, g.host, kT.Payment), y = new GT(this.messageBus, "cardForm"), this.context.interactionsNotifier = y, m = this.appendPaymentButtons(g, c, y), b = !!m, m && m.then(function () {
                    return h.buttonsLoadEnded(b);
                  }), k = this.trace.addSpan("ReadyMessage", "function"), e.abrupt("return", Promise.race([c.unmounted().then(function () {
                    var e;
                    P.isCompleted || (null === (e = P.trace) || void 0 === e || e.finish(Pk.Cancelled), P.onFail(new QP("".concat(P.paymentButtonsExist ? "Unable to append payment buttons: " : "", "Payment form iframe was removed from DOM before initialization ended"))));
                  }), new Promise(function (e) {
                    var t = function () {
                      var n = l(s().mark(function n(r) {
                        var i, o;
                        return s().wrap(function (n) {
                          for (;;) switch (n.prev = n.next) {
                            case 0:
                              if (r.type === DP.FormReady) {
                                n.next = 2;
                                break;
                              }
                              return n.abrupt("return");
                            case 2:
                              if (!1 !== (null === (i = P.config.formParams) || void 0 === i ? void 0 : i.enabled) && c.show(), P.messageBus.sendPrivateMessage({
                                type: bP.RequestSize
                              }, c.getWindow()), xT(function () {
                                return c.enableTransitions();
                              }), k.finish(), h.formLoadEnded(b), r.integrity === a) {
                                n.next = 12;
                                break;
                              }
                              return P.readyMessageState = "Foreign", n.abrupt("return");
                            case 12:
                              P.readyMessageState = "Ask";
                            case 13:
                              if (P.messageBus.unsubscribe(t), P.messageBus.sendPublicMessage({
                                type: bP.Mounted,
                                entity: eT.Form
                              }), P.tracking.domainsUsage({
                                pageUrl: P.locationService.getPageUrl(),
                                sdkReferrer: P.locationService.getSdkReferrer()
                              }), P.tracking.legacyBrowsersTest(), e(), P.onSuccess(), !m) {
                                n.next = 22;
                                break;
                              }
                              return n.next = 22, m;
                            case 22:
                              null === (o = P.trace) || void 0 === o || o.finish();
                            case 23:
                            case "end":
                              return n.stop();
                          }
                        }, n);
                      }));
                      return function (e) {
                        return n.apply(this, arguments);
                      };
                    }();
                    P.messageBus.subscribeForPrivate(t), c.onLoad(function () {
                      return P.messageBus.sendPrivateMessage({
                        type: bP.SetPaymentIntent,
                        paymentIntent: g
                      }, c.getWindow());
                    }), c.onError(function (n) {
                      var r,
                        i = new ST();
                      P.logger.error(new QP("Failed to load iframe ".concat(P.branding.getIframeUrl(), ": ").concat(n))), P.context.sendErrorToMerchant(i), P.messageBus.unsubscribe(t), null === (r = P.trace) || void 0 === r || r.finish(Pk.DataLoss), P.onFail(i), e();
                    });
                  })]));
                case 46:
                case "end":
                  return e.stop();
              }
            }, e, this);
          }));
          return function () {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "appendPaymentButtons",
        value: function (e, t, n) {
          var r = {};
          if ("new" === e.status) {
            if ((r = this.makePaymentButtons(t, n, e).appendPaymentButtons()).applePay) {
              var i,
                o = null === (i = this.trace) || void 0 === i ? void 0 : i.addSpan("ApplePayButtonLoading", "resource");
              r.applePay.then(function () {
                null == o || o.finish();
              });
            }
            if (r.googlePay) {
              var a,
                s = null === (a = this.trace) || void 0 === a ? void 0 : a.addSpan("GooglePayButtonLoading", "resource");
              r.googlePay.then(function () {
                null == s || s.finish();
              });
            }
            if (r.paypal) {
              var u,
                c = null === (u = this.trace) || void 0 === u ? void 0 : u.addSpan("PaypalButtonLoading", "resource");
              r.paypal.then(function () {
                null == c || c.finish();
              });
            }
          }
          return 0 === Object.values(r).length ? null : Promise.all(Object.values(r));
        }
      }, {
        key: "makePaymentButtons",
        value: function (e, t, n) {
          var r = new nT({
            language: n.appearance.language,
            wallets: n.wallets,
            clientSide: {
              google: this.config.googlePayButtonParams,
              apple: this.config.applePayButtonParams,
              paypal: this.config.paypalButtonParams
            },
            app: {
              apple: {
                createSessionUrl: "".concat(this.branding.getPaymentFormUrl(), "/api/v2/").concat(n.host, "/apple-pay/session/").concat(n.id)
              },
              paypal: {
                baseApiPath: this.branding.getAltGateBaseUrl()
              }
            },
            collect: {
              zip: n.appearance.collectZip,
              email: n.appearance.collectEmail
            }
          }, n.token, this.release, new DT(e, this.logger, this.merchantLogger), e, this.tracking, this.logger, t, this.messageBus);
          return this.context.paymentsButtons = r, r;
        }
      }, {
        key: "validate",
        value: function () {
          var e,
            t,
            n,
            r = this;
          if (!this.config) {
            var i = new CT("Missing required arguments during initialization");
            return this.merchantLogger.error(i), [!1, i];
          }
          if (this.config.formParams) {
            var o = new QT(),
              a = new eO(),
              s = w(o.validate(this.config.formParams), 2),
              u = s[0],
              c = s[1],
              l = w(a.validate(this.config.formParams), 2),
              f = l[0],
              h = l[1];
            if (!u) {
              var d = new CT("Unsupported formParams values for fields: '".concat(Object.keys(c).join("', '"), "'"));
              this.merchantLogger.error(d, c);
            }
            if (!f) {
              var p = new CT("Unsupported formParams values for fields: '".concat(Object.keys(h).join("', '"), "'"));
              this.logger.error(p, h);
            }
          }
          return null !== (e = this.config.formParams) && void 0 !== e && e.buttonType && !Object.values(bT).some(function (e) {
            var t;
            return e === (null === (t = r.config.formParams) || void 0 === t ? void 0 : t.buttonType);
          }) && (this.merchantLogger.error(new CT("Unsupported formParams.buttonType, switching to default")), this.config.formParams.buttonType = bT.Default), null !== (t = this.config.formParams) && void 0 !== t && t.formTypeClass && !Object.values(wT).includes(null === (n = this.config.formParams) || void 0 === n ? void 0 : n.formTypeClass) && (this.merchantLogger.error(new CT("Unsupported formParams.formTypeClass, switching to default")), this.config.formParams.formTypeClass = wT.Default), [!0];
        }
      }, {
        key: "mountIframe",
        value: function () {
          var e = l(s().mark(function e(t, n) {
            var r, i, o, a, u, c, l, f;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  if (t.mount(n, null === (r = this.config.iframeParams) || void 0 === r ? void 0 : r.containerId, null === (i = this.config.iframeParams) || void 0 === i ? void 0 : i.width), "Mounted" === t.state) {
                    e.next = 6;
                    break;
                  }
                  return this.merchantLogger.warning("Retry creating iframe in 1 ms"), e.next = 5, PT(1);
                case 5:
                  t.mount(n, null === (o = this.config.iframeParams) || void 0 === o ? void 0 : o.containerId, null === (a = this.config.iframeParams) || void 0 === a ? void 0 : a.width);
                case 6:
                  if ("Mounted" === t.state) {
                    e.next = 11;
                    break;
                  }
                  return this.merchantLogger.warning("Retry creating iframe in 10 ms"), e.next = 10, PT(10);
                case 10:
                  t.mount(n, null === (u = this.config.iframeParams) || void 0 === u ? void 0 : u.containerId, null === (c = this.config.iframeParams) || void 0 === c ? void 0 : c.width);
                case 11:
                  if ("Mounted" === t.state) {
                    e.next = 16;
                    break;
                  }
                  return this.merchantLogger.warning("Retry creating iframe in 50 ms"), e.next = 15, PT(50);
                case 15:
                  t.mount(n, null === (l = this.config.iframeParams) || void 0 === l ? void 0 : l.containerId, null === (f = this.config.iframeParams) || void 0 === f ? void 0 : f.width);
                case 16:
                  "Mounted" !== t.state && this.merchantLogger.warning("Giving up retry creating iframe");
                case 17:
                case "end":
                  return e.stop();
              }
            }, e, this);
          }));
          return function (t, n) {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "logLongExecution",
        value: function () {
          var e = this,
            t = this.trace;
          setTimeout(function () {
            e.isCompleted || (e.logger.withinContext(t, function () {
              var t;
              return e.logger.error(new QP("Initialization took more than 90 seconds, iframe: ".concat(null === (t = e.iframe) || void 0 === t ? void 0 : t.state, ", ready message: ").concat(e.readyMessageState)));
            }), null == t || t.finish(Pk.InternalError), e.onFail(new QP("Internal error")));
          }, 9e4);
        }
      }]);
    }(yT),
    nO = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, [e])).name = "FormResignDtoError", r;
      }
      return g(n, e), d(n);
    }(m(Error)),
    rO = function (e) {
      function n() {
        return f(this, n), t(this, n, [{
          autoFocus: KT.oneOf([!0, !1, "true"]),
          submitButtonText: KT.string,
          allowSubmit: KT.oneOf([!0, !1, "true"]),
          googleFontLink: KT.string,
          resignCvvLabel: KT.string,
          resignCvvPlaceholder: KT.string,
          hideCvvNumbers: KT.oneOf([!0, !1, "true"])
        }]);
      }
      return g(n, e), d(n);
    }(KT),
    iO = function (e) {
      function n() {
        return f(this, n), t(this, n, [{
          autoFocus: KT.boolean,
          submitButtonText: KT.string,
          allowSubmit: KT.boolean,
          googleFontLink: KT.string,
          resignCvvLabel: KT.string,
          resignCvvPlaceholder: KT.string,
          hideCvvNumbers: KT.boolean
        }]);
      }
      return g(n, e), d(n);
    }(KT),
    oO = function () {
      return d(function e(t, n, r, i) {
        var o, a;
        f(this, e), this.resign = t, this.branding = n, this.sdkVersion = r, this.logger = i, this.payload = {}, this.initType = null !== (o = n.getSdkInitType()) && void 0 !== o ? o : HT.Default, this.addMerchantStyles(null === (a = this.resign.formConfig) || void 0 === a ? void 0 : a.styles), this.verifyInitType(), this.addMetadata();
      }, [{
        key: "toJSON",
        value: function (e) {
          return {
            type: bP.FormInitialization,
            paymentType: kT.Resign,
            formConfig: a(a({}, this.resign.formConfig), {}, {
              styles: this.inlineStyles
            }),
            integrity: e
          };
        }
      }, {
        key: "toApiCall",
        value: function () {
          return a(a({}, this.resign.request), {}, {
            sdkVersion: this.sdkVersion,
            meta: this.payload.meta
          });
        }
      }, {
        key: "styles",
        get: function () {
          return this.inlineStyles;
        }
      }, {
        key: "addMerchantStyles",
        value: function (e) {
          if (e) {
            var t = ZT(e);
            Object.keys(t).length && (this.inlineStyles = t);
          }
        }
      }, {
        key: "addMetadata",
        value: function () {
          var e;
          this.payload.meta = {
            isFrameworkSdkUsed: !!this.branding.getSdkInitType(),
            cdn: this.branding.getCdnList(),
            customContainerId: (null === (e = this.resign.formConfig) || void 0 === e || null === (e = e.container) || void 0 === e ? void 0 : e.id) || this.branding.getDefaultFormId()
          };
        }
      }, {
        key: "verifyInitType",
        value: function () {
          var e = this;
          Object.values(HT).some(function (t) {
            return t === e.initType;
          }) || (this.logger.error(new CT("Unrecognized init type ".concat(this.initType))), this.initType = HT.Default);
        }
      }]);
    }(),
    aO = function (e) {
      function n(e, r, i, o, a, s, u, c, l, h, d, p) {
        var g;
        return f(this, n), (g = t(this, n)).config = e, g.context = r, g.api = i, g.tracking = o, g.messageBus = a, g.logger = s, g.merchantLogger = u, g.branding = c, g.uuid = l, g.release = h, g.iframePool = d, g.locationService = p, g.readyMessageState = "Initial", g.iframe = null, g.trace = null, g;
      }
      return g(n, e), d(n, [{
        key: "execute",
        value: function () {
          var e = l(s().mark(function e() {
            var t,
              n,
              r,
              i,
              o,
              a,
              u,
              c,
              f,
              h,
              d,
              p,
              g,
              v,
              y,
              m,
              b,
              k,
              P = this;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  if (this.context.initialized && this.context.flush(), this.context.initialized = !0, r = this.validate(), i = w(r, 2), o = i[0], a = i[1], o) {
                    e.next = 6;
                    break;
                  }
                  return this.onFail(a), e.abrupt("return");
                case 6:
                  if (u = new oO(this.config, this.branding, this.release, this.logger), c = this.uuid(), this.trace = this.logger.trace("ResignInitialization-v2"), f = this.tracking.resignInitTime(), this.logLongExecution(), this.context.resignConfig = this.config, h = this.trace.addSpan("IframeLoading", "resource"), d = this.iframePool.getIframe(), this.context.iframe = d, p = this.config.formConfig, d.mount(c, null == p || null === (t = p.container) || void 0 === t ? void 0 : t.id, null == p || null === (n = p.container) || void 0 === n ? void 0 : n.width), "Mounted" === d.state) {
                    e.next = 21;
                    break;
                  }
                  return this.trace.finish(Pk.NotFound), this.onFail(new QP("Element with containerId: ".concat(null == p || null === (g = p.container) || void 0 === g ? void 0 : g.id, " is missing"))), e.abrupt("return");
                case 21:
                  return this.iframe = d, d.onLoad(function () {
                    P.tracking.scriptLoadTime(), P.messageBus.sendPrivateMessage(u.toJSON(c), d.getWindow()), h.finish();
                  }), v = this.trace.addSpan("InitResignRequest", "http"), e.next = 26, this.api.resign(u.toApiCall());
                case 26:
                  if (y = e.sent, m = y.result, b = y.retries, !(m instanceof Error)) {
                    e.next = 34;
                    break;
                  }
                  return this.context.sendErrorToMerchant(m), this.onFail(m), this.trace.finish(Pk.PermissionDenied), e.abrupt("return");
                case 34:
                  return this.tracking.initNetworkError(b), v.finish(), this.context.intent = m, m.tracking && this.tracking.init(m.tracking.trackSignature, m.tracking.trackId), d.setIntentMetadata(m.id, m.host, kT.Resign), this.context.interactionsNotifier = new GT(this.messageBus, "resignForm"), k = this.trace.addSpan("ReadyMessage", "function"), e.abrupt("return", Promise.race([d.unmounted().then(function () {
                    var e;
                    P.isCompleted || (null === (e = P.trace) || void 0 === e || e.finish(Pk.Cancelled), P.onFail(new QP("Payment form iframe was removed from DOM before initialization ended")));
                  }), new Promise(function (e) {
                    var t = function () {
                      var n = l(s().mark(function n(r) {
                        var i;
                        return s().wrap(function (n) {
                          for (;;) switch (n.prev = n.next) {
                            case 0:
                              if (r.type === DP.FormReady) {
                                n.next = 2;
                                break;
                              }
                              return n.abrupt("return");
                            case 2:
                              if (d.show(), xT(function () {
                                return d.enableTransitions();
                              }), k.finish(), f(), r.integrity === c) {
                                n.next = 12;
                                break;
                              }
                              return P.readyMessageState = "Foreign", P.logger.error(new QP("Foreign message received"), {
                                expected: c,
                                actual: r.integrity
                              }), n.abrupt("return");
                            case 12:
                              P.readyMessageState = "Ask";
                            case 13:
                              P.messageBus.unsubscribe(t), P.messageBus.sendPublicMessage({
                                type: bP.Mounted,
                                entity: eT.Resign
                              }), P.tracking.domainsUsage({
                                pageUrl: P.locationService.getPageUrl(),
                                sdkReferrer: P.locationService.getSdkReferrer()
                              }), P.tracking.legacyBrowsersTest(), e(), P.onSuccess(), null === (i = P.trace) || void 0 === i || i.finish();
                            case 20:
                            case "end":
                              return n.stop();
                          }
                        }, n);
                      }));
                      return function (e) {
                        return n.apply(this, arguments);
                      };
                    }();
                    P.messageBus.subscribeForPrivate(t), d.onLoad(function () {
                      return P.messageBus.sendPrivateMessage({
                        type: bP.SetResignIntent,
                        resignIntent: m
                      }, d.getWindow());
                    }), d.onError(function (n) {
                      var r,
                        i = new ST();
                      P.logger.error(new QP("Failed to load iframe ".concat(P.branding.getIframeUrl(), ": ").concat(n))), P.context.sendErrorToMerchant(i), P.messageBus.unsubscribe(t), null === (r = P.trace) || void 0 === r || r.finish(Pk.DataLoss), P.onFail(i), e();
                    });
                  })]));
                case 42:
                case "end":
                  return e.stop();
              }
            }, e, this);
          }));
          return function () {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "validate",
        value: function () {
          var e;
          if (null === (e = this.config) || void 0 === e || !e.request) {
            var t = new nO("Missing config request argument");
            return this.merchantLogger.error(t), [!1, t];
          }
          if (this.config.formConfig.appearance) {
            var n = new iO(),
              r = new rO(),
              i = w(n.validate(this.config.formConfig.appearance), 2),
              o = i[0],
              a = i[1],
              s = w(r.validate(this.config.formConfig.appearance), 2),
              u = s[0],
              c = s[1];
            if (!o) {
              var l = new nO("Unsupported formConfig.appearance values for fields: '".concat(Object.keys(a).join("', '"), "'"));
              this.merchantLogger.error(l, a);
            }
            if (!u) {
              var f = new nO("Unsupported formConfig.appearance values for fields: '".concat(Object.keys(c).join("', '"), "'"));
              this.logger.error(f, c);
            }
          }
          return [!0];
        }
      }, {
        key: "logLongExecution",
        value: function () {
          var e = this,
            t = this.trace;
          setTimeout(function () {
            e.isCompleted || (e.logger.withinContext(t, function () {
              var t;
              return e.logger.error(new QP("Resign initialization took more than 90 seconds, iframe: ".concat(null === (t = e.iframe) || void 0 === t ? void 0 : t.state, ", ready message: ").concat(e.readyMessageState)));
            }), null == t || t.finish(Pk.InternalError), e.onFail(new QP("Internal error")));
          }, 9e4);
        }
      }]);
    }(yT),
    sO = function (e) {
      var t = e;
      return t.type === DP.UpdateComplete && !!t.error;
    },
    uO = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, [e])).name = "UpdateDtoError", r;
      }
      return g(n, e), d(n);
    }(m(Error)),
    cO = function () {
      function e(t) {
        f(this, e), this.updateConfig = t;
      }
      return d(e, [{
        key: "validate",
        value: function () {
          return this.validatePartialIntent() ? this.validateButtonType() ? this.validateFormTypeClass() ? this.validateApplePayButtonParams() ? [!0] : [!1, new uO("Unsupported applePayButtonParams.type")] : [!1, new uO("Unsupported formParams.formTypeClass")] : [!1, new uO("Unsupported formParams.buttonType")] : [!1, new uO("Unable to perform update: Missing intent or signature")];
        }
      }, {
        key: "toJSON",
        value: function () {
          var t,
            n,
            r = this.updateConfig,
            i = r.partialIntent,
            o = r.signature,
            a = r.formParams,
            s = r.styles;
          s && (t = null !== (n = e.getInlineStyles(s)) && void 0 !== n ? n : null);
          return {
            partialIntent: i,
            signature: o,
            formParams: a,
            styles: t
          };
        }
      }, {
        key: "applePayButtonParams",
        get: function () {
          return this.updateConfig.applePayButtonParams;
        }
      }, {
        key: "validatePartialIntent",
        value: function () {
          return !this.updateConfig.partialIntent && !this.updateConfig.signature || !(!this.updateConfig.partialIntent || !this.updateConfig.signature);
        }
      }, {
        key: "validateFormParams",
        value: function () {
          var e = new QT();
          return this.updateConfig.formParams ? e.validate(this.updateConfig.formParams) : [!0];
        }
      }, {
        key: "looseValidateFormParams",
        value: function () {
          var e = new eO();
          return this.updateConfig.formParams ? e.validate(this.updateConfig.formParams) : [!0];
        }
      }, {
        key: "validateButtonType",
        value: function () {
          var e,
            t = this;
          return !(null !== (e = this.updateConfig.formParams) && void 0 !== e && e.buttonType && !Object.values(bT).some(function (e) {
            var n;
            return e === (null === (n = t.updateConfig.formParams) || void 0 === n ? void 0 : n.buttonType);
          }));
        }
      }, {
        key: "validateFormTypeClass",
        value: function () {
          var e, t;
          return !(null !== (e = this.updateConfig.formParams) && void 0 !== e && e.formTypeClass && !Object.values(wT).includes(null === (t = this.updateConfig.formParams) || void 0 === t ? void 0 : t.formTypeClass));
        }
      }, {
        key: "validateApplePayButtonParams",
        value: function () {
          var e, t;
          return !(null !== (e = this.updateConfig.applePayButtonParams) && void 0 !== e && e.type && $C.forbiddenTypes.includes(null === (t = this.updateConfig.applePayButtonParams) || void 0 === t ? void 0 : t.type));
        }
      }], [{
        key: "getInlineStyles",
        value: function (e) {
          if (e) {
            var t = ZT(e);
            if (Object.keys(t).length) return t;
          }
        }
      }]);
    }(),
    lO = function (e) {
      function n(e, r, i, o, a, s) {
        var u;
        return f(this, n), (u = t(this, n)).context = r, u.logger = i, u.tracking = o, u.merchantLogger = a, u.messageBus = s, u.trace = null, u.updateDto = new cO(e), u;
      }
      return g(n, e), d(n, [{
        key: "execute",
        value: function () {
          var e = l(s().mark(function e() {
            var t,
              n,
              r,
              i,
              o,
              a,
              u = this;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  if (this.trace = this.logger.trace("Update"), this.logLongExecution(), t = this.context.paymentsButtons, this.tracking.updateIntentStarted(), null === (n = this.validate())) {
                    e.next = 9;
                    break;
                  }
                  return r = w(n, 2), i = r[0], o = r[1], this.handleFail(o, i), e.abrupt("return");
                case 9:
                  return null == t || t.setIsDisabled(!0), this.startUpdateInIframe(), a = this.tracking.updateTime(), e.abrupt("return", Promise.race([this.context.iframe.unmounted().then(function () {
                    u.isCompleted || u.handleFail(new QP("Payment form iframe was removed from DOM before update ended"), Pk.Cancelled);
                  }), this.updateInIframeCompleted().then(function (e) {
                    u.isCompleted || (sO(e) ? u.handleFail(e.error, Pk.InvalidArgument) : (u.handleSuccess(e, t), a()));
                  })]));
                case 13:
                case "end":
                  return e.stop();
              }
            }, e, this);
          }));
          return function () {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "logLongExecution",
        value: function () {
          var e = this,
            t = this.trace;
          setTimeout(function () {
            e.isCompleted || (e.logger.withinContext(t, function () {
              e.logger.error(new QP("Update took more than 90 seconds, giving up"));
            }), t.finish(Pk.InternalError), e.onFail(new QP("Internal error during update")));
          }, 9e4);
        }
      }, {
        key: "validate",
        value: function () {
          var e;
          if (this.context.resignConfig) return [Pk.FailedPrecondition, new QP("Resign intents does not support update")];
          if (!this.context.intent) return [Pk.FailedPrecondition, new QP("Cannot update uninitialized form")];
          var t = w(this.updateDto.validate(), 2),
            n = t[0],
            r = t[1],
            i = w(this.updateDto.validateFormParams(), 2),
            o = i[0],
            a = i[1],
            s = w(this.updateDto.looseValidateFormParams(), 2),
            u = s[0],
            c = s[1];
          if (!o) {
            var l = new uO("Unsupported formParams values for fields: '".concat(Object.keys(a).join("', '"), "'"));
            this.merchantLogger.error(l, a);
          }
          if (!u) {
            var f = new uO("Unsupported formParams values for fields: '".concat(Object.keys(c).join("', '"), "'"));
            this.logger.error(f, c);
          }
          return n ? null !== (e = this.context.iframe) && void 0 !== e && e.isPresentInDOM() ? null : [Pk.Cancelled, new QP("Unable to perform update: payment form iframe not found")] : [Pk.Cancelled, r];
        }
      }, {
        key: "handleFail",
        value: function (e, t) {
          var n;
          null === (n = this.trace) || void 0 === n || n.finish(t), this.onFail(e);
        }
      }, {
        key: "handleSuccess",
        value: function (e, t) {
          var n,
            r = {};
          if (function (e) {
            var t = e;
            return t.type === DP.UpdateComplete && !(!t.amount || !t.currency);
          }(e)) {
            var i = e.amount,
              o = e.currency;
            r.price = {
              amount: i,
              currency: o
            };
          }
          var a = this.updateDto.applePayButtonParams;
          a && (r.appearance = {}, a && (r.appearance.applePay = {
            buttonColor: null == a ? void 0 : a.color,
            buttonType: null == a ? void 0 : a.type
          })), null == t || t.update(r), null == t || t.setIsDisabled(!1), null === (n = this.trace) || void 0 === n || n.finish(), this.onSuccess();
        }
      }, {
        key: "startUpdateInIframe",
        value: function () {
          var e;
          this.messageBus.sendPrivateMessage({
            type: bP.UpdatePaymentIntent,
            payload: this.updateDto.toJSON()
          }, null === (e = this.context.iframe) || void 0 === e ? void 0 : e.getWindow());
        }
      }, {
        key: "updateInIframeCompleted",
        value: function () {
          var e = this;
          return new Promise(function (t) {
            e.messageBus.subscribeForPrivate(function n(r) {
              r.type === DP.UpdateComplete && (e.messageBus.unsubscribe(n), t(r));
            });
          });
        }
      }]);
    }(yT),
    fO = function () {
      return d(function e() {
        f(this, e);
      }, [{
        key: "error",
        value: function (e, t) {
          console.error(e, t);
        }
      }, {
        key: "warning",
        value: function (e, t) {
          console.warn(e, t);
        }
      }, {
        key: "debug",
        value: function (e) {
          console.debug(e);
        }
      }]);
    }(),
    hO = function (e) {
      function n() {
        var e;
        return f(this, n), (e = t(this, n, arguments)).name = "GatewayError", e.message = "Something went wrong on our side. Please contact support", e;
      }
      return g(n, e), d(n);
    }(m(Error)),
    dO = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, ["Unable to init resign: ".concat(JSON.stringify(e))])).name = "InitResignError", r.details = e, r;
      }
      return g(n, e), d(n);
    }(m(Error)),
    pO = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, [e])).name = "SdkApiError", r;
      }
      return g(n, e), d(n);
    }(m(Error));
  function gO(e) {
    return void 0 !== e.error;
  }
  var vO,
    yO = function () {
      return d(function e(t, n, r) {
        f(this, e), this.logger = t, this.urls = n, this.release = r;
      }, [{
        key: "init",
        value: function () {
          var e = l(s().mark(function e(t) {
            var n, r, i, o, u, c;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  return r = this.getInitPaymentPayload(t), e.next = 3, this.request({
                    url: this.urls.init,
                    body: JSON.stringify(r),
                    merchant: t.merchant,
                    signature: t.signature
                  });
                case 3:
                  if (i = e.sent, o = i.result, u = i.retries, !(o instanceof Error)) {
                    e.next = 8;
                    break;
                  }
                  return e.abrupt("return", {
                    result: o,
                    retries: u
                  });
                case 8:
                  if (!gO(o)) {
                    e.next = 10;
                    break;
                  }
                  return e.abrupt("return", {
                    result: new sx(o.error),
                    retries: u
                  });
                case 10:
                  return c = o.data, null !== (n = c.wallets) && void 0 !== n && n.paypal && (c.wallets.paypal = a(a({}, c.wallets.paypal), {}, {
                    fraudnetSessionId: c.id,
                    currency: c.price.currency
                  })), e.abrupt("return", {
                    result: c,
                    retries: u
                  });
                case 13:
                case "end":
                  return e.stop();
              }
            }, e, this);
          }));
          return function (t) {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "resign",
        value: function () {
          var e = l(s().mark(function e(t) {
            var n, r, i, o;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  return n = this.getResignPayload(t), e.next = 3, this.request({
                    url: this.urls.resign,
                    body: JSON.stringify(n),
                    merchant: t.merchant,
                    signature: t.signature
                  });
                case 3:
                  if (r = e.sent, i = r.result, o = r.retries, !(i instanceof Error)) {
                    e.next = 8;
                    break;
                  }
                  return e.abrupt("return", {
                    result: i,
                    retries: o
                  });
                case 8:
                  if (!gO(i)) {
                    e.next = 10;
                    break;
                  }
                  return e.abrupt("return", {
                    result: new dO(i.error),
                    retries: o
                  });
                case 10:
                  return e.abrupt("return", {
                    result: i.data,
                    retries: o
                  });
                case 11:
                case "end":
                  return e.stop();
              }
            }, e, this);
          }));
          return function (t) {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "getInitPaymentPayload",
        value: function (e) {
          var t = {
            payment_intent: e.paymentIntent,
            version: e.version || "v1",
            sdk_version: e.sdkVersion
          };
          return e.meta && (t.meta = {
            is_brand_logo_defined: e.meta.isBrandLogoDefined,
            is_framework_sdk_used: e.meta.isFrameworkSdkUsed,
            cdn: e.meta.cdn,
            custom_container_id: e.meta.customContainerId
          }), t;
        }
      }, {
        key: "request",
        value: function () {
          var e = l(s().mark(function e(t) {
            var n, r, i, o;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  return r = 0, e.prev = 1, i = new QE({
                    url: t.url,
                    method: "POST",
                    headers: {
                      Merchant: t.merchant,
                      Signature: t.signature,
                      "X-Release": this.release
                    },
                    body: t.body
                  }, {
                    times: 5,
                    time: 2e3,
                    whenOnline: !0,
                    shouldRepeat: function (e) {
                      return 400 !== e && (r += 1, null === e || e >= 300);
                    }
                  }), e.next = 5, i.execute();
                case 5:
                  n = e.sent, e.next = 12;
                  break;
                case 8:
                  return e.prev = 8, e.t0 = e.catch(1), this.logNetworkError(null), e.abrupt("return", {
                    retries: r,
                    result: new ST()
                  });
                case 12:
                  if (n.status && ![403, 502, 504].includes(n.status) || this.logNetworkError(n.status), n.ok || 400 === n.status) {
                    e.next = 15;
                    break;
                  }
                  return e.abrupt("return", {
                    retries: r,
                    result: new hO()
                  });
                case 15:
                  return e.prev = 15, e.next = 18, n.json();
                case 18:
                  o = e.sent, e.next = 25;
                  break;
                case 21:
                  return e.prev = 21, e.t1 = e.catch(15), this.logger.error(e.t1), e.abrupt("return", {
                    retries: r,
                    result: new hO()
                  });
                case 25:
                  return e.abrupt("return", {
                    result: o,
                    retries: r
                  });
                case 26:
                case "end":
                  return e.stop();
              }
            }, e, this, [[1, 8], [15, 21]]);
          }));
          return function (t) {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "getResignPayload",
        value: function (e) {
          var t = {
            payment_intent: e.resignIntent,
            version: e.version || "v1",
            sdk_version: e.sdkVersion
          };
          return e.meta && (t.meta = {
            is_framework_sdk_used: e.meta.isFrameworkSdkUsed,
            cdn: e.meta.cdn,
            custom_container_id: e.meta.customContainerId
          }), t;
        }
      }, {
        key: "logNetworkError",
        value: function (e) {
          this.logger.error(new pO("Network error"), {
            status: e || "empty"
          });
        }
      }]);
    }(),
    mO = ["localhost", "127.0.0.1"],
    bO = d(function e() {
      f(this, e);
    });
  (vO = bO).toSnakeCase = function (e) {
    return e.replace(/[A-Z]/g, function (e) {
      return "_".concat(e.toLowerCase());
    });
  }, vO.toCamelCase = function (e) {
    return e.replace(/([-_][a-z])/gi, function (e) {
      return e.toUpperCase().replace("-", "").replace("_", "");
    });
  };
  var wO,
    kO = function (e) {
      function n(e) {
        var r;
        return f(this, n), (r = t(this, n, [e])).name = "TrackingApiError", r;
      }
      return g(n, e), d(n);
    }(m(Error)),
    PO = function () {
      return d(function e() {
        f(this, e), this.lock = Promise.resolve(), this.resolveLock = function () {};
      }, [{
        key: "acquire",
        value: function () {
          var e = l(s().mark(function e() {
            var t = this;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  return e.next = 2, this.lock;
                case 2:
                  this.lock = new Promise(function (e) {
                    t.resolveLock = e;
                  });
                case 3:
                case "end":
                  return e.stop();
              }
            }, e, this);
          }));
          return function () {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "release",
        value: function () {
          this.resolveLock();
        }
      }]);
    }(),
    xO = function () {
      function e(t, n) {
        f(this, e), this.queueMutex = new PO(), this.queue = [], this.logger = n, this.config = {
          url: t
        }, this.messageEnrichment = {
          sessionId: this.makeId(e.IdLength),
          signature: "",
          entityName: "",
          entityValue: ""
        };
      }
      return d(e, [{
        key: "keysToSnake",
        value: function (e) {
          var t = this;
          if (function (e) {
            return e === Object(e) && !Array.isArray(e) && "function" != typeof e;
          }(e)) {
            var n = {};
            return Object.keys(e).forEach(function (r) {
              n[bO.toSnakeCase(r)] = t.keysToSnake(e[r]);
            }), n;
          }
          return Array.isArray(e) ? e.map(function (e) {
            return t.keysToSnake(e);
          }) : e;
        }
      }, {
        key: "init",
        value: function (t, n, r) {
          var i = this;
          this.messageEnrichment.signature = t, this.messageEnrichment.entityValue = n, this.messageEnrichment.entityName = r, this.queue = this.queue.map(function (t) {
            return e.isEnrichedMessage(t) ? t : i.enrichMessage(t);
          }), this.drainQueue();
        }
      }, {
        key: "clear",
        value: function () {
          this.messageEnrichment.signature = "", this.messageEnrichment.entityValue = "", this.messageEnrichment.entityName = "";
        }
      }, {
        key: "send",
        value: function (e) {
          this.queue.push(this.enrichMessage(e)), this.drainQueue();
        }
      }, {
        key: "getEventISOTime",
        value: function () {
          return new Date().toISOString().slice(0, -1);
        }
      }, {
        key: "warmupOptionsCache",
        value: function () {
          var e = l(s().mark(function e() {
            var t;
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  return e.next = 2, this.queueMutex.acquire();
                case 2:
                  return t = new QE({
                    url: this.config.url,
                    method: "OPTIONS",
                    headers: {
                      "Content-Type": "application/json",
                      Signature: "CORS-WARMUP-SIGNATURE"
                    }
                  }), e.prev = 3, e.next = 6, t.execute();
                case 6:
                  e.next = 11;
                  break;
                case 8:
                  e.prev = 8, e.t0 = e.catch(3), e.t0 instanceof Error && this.logger.error(new kO(e.t0.toString()), a(a({}, e.t0), {}, {
                    source: "Unsent analytics"
                  }));
                case 11:
                  this.queueMutex.release();
                case 12:
                case "end":
                  return e.stop();
              }
            }, e, this, [[3, 8]]);
          }));
          return function () {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "drainQueue",
        value: function () {
          var t = l(s().mark(function t() {
            var n,
              r,
              i,
              o = this;
            return s().wrap(function (t) {
              for (;;) switch (t.prev = t.next) {
                case 0:
                  return t.next = 2, this.queueMutex.acquire();
                case 2:
                  return t.next = 4, new Promise(function (t) {
                    return setTimeout(t, e.BatchCollectTimeMs);
                  });
                case 4:
                  n = e.getBatches(this.queue), r = w(n, 2), i = r[0], r[1].forEach(function (e) {
                    try {
                      o.request(e).catch(function (e) {
                        e instanceof Error && o.logger.error(new kO(e.toString()), e);
                      });
                    } catch (DO) {
                      DO instanceof Error && o.logger.error(new kO(DO.toString()), DO);
                    }
                  }), this.queue = i, this.queueMutex.release();
                case 8:
                case "end":
                  return t.stop();
              }
            }, t, this);
          }));
          return function () {
            return t.apply(this, arguments);
          };
        }()
      }, {
        key: "makeId",
        value: function (e) {
          for (var t = "", n = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", r = 0; r < e; r++) t += n.charAt(Math.floor(62 * Math.random()));
          return t;
        }
      }, {
        key: "enrichMessage",
        value: function (e) {
          return a(a({}, e), {}, {
            sessionId: this.messageEnrichment.sessionId,
            entityName: e.entityName || this.messageEnrichment.entityName,
            entityValue: e.entityValue || this.messageEnrichment.entityValue,
            signature: e.signature || this.messageEnrichment.signature,
            event_time: e.event_time || this.getEventISOTime()
          });
        }
      }, {
        key: "request",
        value: function (e) {
          var t = this;
          if (!this.config.url) return Promise.resolve();
          var n = e.map(function (e) {
            return t.keysToSnake({
              sessionId: e.sessionId,
              entityName: e.entityName,
              entityValue: e.entityValue,
              event: e.event,
              category: e.category,
              level: e.level,
              context: e.context,
              eventTime: e.event_time,
              signature: e.signature,
              value: e.value
            });
          });
          return new QE({
            url: "".concat(this.config.url, "batch"),
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              events: n
            })
          }).execute().catch(function (e) {
            e instanceof Error && t.logger.error(new kO(e.toString()), a(a({}, e), {}, {
              source: "Unsent analytics"
            }));
          });
        }
      }], [{
        key: "isEnrichedMessage",
        value: function (e) {
          return !!e.signature;
        }
      }, {
        key: "getBatches",
        value: function (t) {
          var n = [];
          return [t.filter(function (t) {
            if (!e.isEnrichedMessage(t)) return !0;
            var r = n.find(function (t) {
              return t.length < e.BatchMaxLength;
            });
            return r || (r = [], n.push(r)), r.push(t), !1;
          }), n];
        }
      }]);
    }();
  (wO = xO).IdLength = 32, wO.BatchMaxLength = 20, wO.BatchCollectTimeMs = 50;
  var SO,
    CO,
    EO = function (e) {
      function n() {
        return f(this, n), t(this, n, arguments);
      }
      return g(n, e), d(n, [{
        key: "init",
        value: function () {}
      }, {
        key: "send",
        value: function () {}
      }]);
    }(xO),
    TO = function () {
      return d(function e(t) {
        f(this, e), this.hostname = t;
      }, [{
        key: "create",
        value: function (e, t) {
          var n,
            r = function (e, t) {
              var n = "undefined" != typeof Symbol && e[Symbol.iterator] || e["@@iterator"];
              if (!n) {
                if (Array.isArray(e) || (n = P(e)) || t) {
                  n && (e = n);
                  var r = 0,
                    i = function () {};
                  return {
                    s: i,
                    n: function () {
                      return r >= e.length ? {
                        done: !0
                      } : {
                        done: !1,
                        value: e[r++]
                      };
                    },
                    e: function (e) {
                      throw e;
                    },
                    f: i
                  };
                }
                throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
              }
              var o,
                a = !0,
                s = !1;
              return {
                s: function () {
                  n = n.call(e);
                },
                n: function () {
                  var e = n.next();
                  return a = e.done, e;
                },
                e: function (e) {
                  s = !0, o = e;
                },
                f: function () {
                  try {
                    a || null == n.return || n.return();
                  } finally {
                    if (s) throw o;
                  }
                }
              };
            }(mO);
          try {
            for (r.s(); !(n = r.n()).done;) {
              var i = n.value;
              if (this.hostname.includes(i)) return new EO(e, t);
            }
          } catch (DO) {
            r.e(DO);
          } finally {
            r.f();
          }
          return new xO(e, t);
        }
      }]);
    }(),
    OO = function () {
      return d(function e(t) {
        f(this, e), this.logger = t, this.isProcessing = !1, this.queue = [], this.currentCase = null;
      }, [{
        key: "execute",
        value: function (e) {
          this.queue.push(e), this.isProcessing || this.process();
        }
      }, {
        key: "process",
        value: function () {
          var e = this;
          this.isProcessing = !0, this.currentCase = this.getUniqueUseCase(), this.currentCase ? this.currentCase.execute().catch(function (t) {
            return e.logger.error(t);
          }).then(function () {
            e.currentCase = null, e.process();
          }) : this.isProcessing = !1;
        }
      }, {
        key: "getUniqueUseCase",
        value: function () {
          for (; this.queue.length;) {
            var e = this.queue.shift(),
              t = this.queue[0];
            if (!e) return null;
            if (!t) return e;
            if (!(e.constructor === t.constructor)) return e;
          }
          return null;
        }
      }]);
    }(),
    IO = new WeakMap(),
    AO = function () {
      return d(function e(t, n, i, o, a) {
        var s = this;
        f(this, e), S(this, IO, void 0), this.logger = t, this.uuid = n, this.isTopmostFrame = window.top === window, this.merchantLogger = new fO(), this.onMessageBusSend = function (e) {
          s.isTopmostFrame || window.postMessage(e, "*");
        }, this.messageBus = new UP({
          onSend: this.onMessageBusSend
        }), this.locationService = new XP(), r(IO, this, i), this.api = new yO(this.logger, {
          init: "".concat(i.getPaymentFormUrl(), "/api/v2/ui/intent"),
          resign: "".concat(i.getPaymentFormUrl(), "/api/v2/ui/resign")
        }, a);
        var u = new TO(window.location.hostname).create(i.getTrackingUrl() || "", this.logger);
        this.tracking = new ix(u, o), this.eventListeners = new qP(this.merchantLogger), this.context = new pT(t, this.merchantLogger, this.messageBus, this.tracking, this.uuid), this.blockingUseCaseInteractor = new OO(this.logger), this.iframePool = new ZP(i, this.merchantLogger, this.messageBus), new ox(this.context, this.tracking, t, this.messageBus);
      }, [{
        key: "init",
        value: function (e) {
          var t = new tO(e, this.context, this.logger, this.api, this.tracking, n(IO, this), this.merchantLogger, this.messageBus, this.uuid, "payment-form-v1.141.0", this.iframePool, this.locationService);
          return this.blockingUseCaseInteractor.execute(t), t.result.catch(function (e) {});
        }
      }, {
        key: "resign",
        value: function (e) {
          var t = new aO({
            request: e,
            formConfig: arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {}
          }, this.context, this.api, this.tracking, this.messageBus, this.logger, this.merchantLogger, n(IO, this), this.uuid, "payment-form-v1.141.0", this.iframePool, this.locationService);
          return this.blockingUseCaseInteractor.execute(t), t.result;
        }
      }, {
        key: "update",
        value: function (e) {
          var t = new lO(e, this.context, this.logger, this.tracking, this.merchantLogger, this.messageBus);
          return this.blockingUseCaseInteractor.execute(t), t.result;
        }
      }, {
        key: "on",
        value: function () {
          var e;
          (e = this.eventListeners).on.apply(e, arguments);
        }
      }, {
        key: "unsubscribe",
        value: function () {
          var e;
          (e = this.eventListeners).unsubscribe.apply(e, arguments);
        }
      }, {
        key: "unsubscribeAll",
        value: function () {
          this.eventListeners.unsubscribeAll();
        }
      }, {
        key: "submit",
        value: function () {
          var e;
          this.messageBus.sendPrivateMessage({
            type: bP.SubmitRequest
          }, null === (e = this.context.iframe) || void 0 === e ? void 0 : e.getWindow());
        }
      }, {
        key: "applyCoupon",
        value: function (e) {
          var t = new mT(e, this.context, this.messageBus, this.logger);
          return this.blockingUseCaseInteractor.execute(t), t.result;
        }
      }, {
        key: "destroyAll",
        value: function () {
          this.unsubscribeAll(), this.context.flush();
        }
      }]);
    }(),
    LO = function () {
      return d(function e(t) {
        f(this, e), SO = t;
      }, [{
        key: "init",
        value: function (e) {
          return SO.init(e);
        }
      }, {
        key: "resign",
        value: function () {
          var e = l(s().mark(function e(t, n) {
            return s().wrap(function (e) {
              for (;;) switch (e.prev = e.next) {
                case 0:
                  return e.next = 2, SO.resign(t, n);
                case 2:
                case "end":
                  return e.stop();
              }
            }, e);
          }));
          return function (t, n) {
            return e.apply(this, arguments);
          };
        }()
      }, {
        key: "destroy",
        value: function () {
          return SO.destroyAll();
        }
      }, {
        key: "update",
        value: function (e) {
          return SO.update(e);
        }
      }, {
        key: "applyCoupon",
        value: function (e) {
          return SO.applyCoupon(e);
        }
      }, {
        key: "on",
        value: function (e, t) {
          SO.on(e, t);
        }
      }, {
        key: "unsubscribe",
        value: function (e) {
          SO.unsubscribe(e);
        }
      }, {
        key: "unsubscribeAll",
        value: function () {
          SO.unsubscribeAll();
        }
      }, {
        key: "submit",
        value: function () {
          SO.submit();
        }
      }]);
    }();
  function jO() {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (e) {
      var t = 16 * Math.random() | 0;
      return ("x" === e ? t : 3 & t | 8).toString(16);
    });
  }
  var RO = "payment-form-v1.141.0",
    BO = (null === (CO = document.currentScript) || void 0 === CO ? void 0 : CO.src) || "",
    _O = new Mw().getBranding(RO, BO),
    NO = new mP(_O.getSentryDSN() || "", RO, "prod", .2),
    FO = null;
  function MO() {
    return (MO = l(s().mark(function e() {
      var t;
      return s().wrap(function (e) {
        for (;;) switch (e.prev = e.next) {
          case 0:
            if (!window.PaymentFormSdk) {
              e.next = 4;
              break;
            }
            return t = new Uw("PaymentFormSdk already inited"), console.warn(t), e.abrupt("return");
          case 4:
            try {
              FO = new LO(new AO(NO, jO, _O, BO, RO));
            } catch (n) {
              NO.error(n);
            }
            window.PaymentFormSdk = {
              init: function (e) {
                return FO.init(e), FO;
              },
              resign: function (e, t) {
                return l(s().mark(function n() {
                  return s().wrap(function (n) {
                    for (;;) switch (n.prev = n.next) {
                      case 0:
                        return n.next = 2, FO.resign(e, t);
                      case 2:
                        return n.abrupt("return", FO);
                      case 3:
                      case "end":
                        return n.stop();
                    }
                  }, n);
                }))();
              },
              destroy: function () {
                FO.destroy();
              }
            };
          case 6:
          case "end":
            return e.stop();
        }
      }, e);
    }))).apply(this, arguments);
  }
  !function () {
    MO.apply(this, arguments);
  }();
});
//# sourceMappingURL=solid-form.js.map
