vardefine,
require;!function(e){
	functionr(e,
	r){
		q(e);vart=tr.waitSeconds;returnj(e)&&t&&(z&&clearTimeout(z),
		z=setTimeout(n,1e3*t)),C(e,r)
	}functionn(){
		vare,
		r=[],
		n=[],
		t={
			
		};for(variinF)f(i)||(e=1,
		r.push(i)),
		A(F[i].depMs||[],
		function(r){
			vari=r.absId;F[i]||t[i]||(e=1,
			n.push(i),
			t[i]=1)
		});if(e)thrownewError("[MODULE_TIMEOUT]Hang( "+(r.join(", ")||"none")+" ) Miss( "+(n.join(", ")||"none")+" )")
	}functiont(){
		vare=arguments.length;if(e){
			for(varr,
			n,
			t=arguments[--e];e--;){
				vari=arguments[e];"string"==typeofi?r=i: j(i)&&(n=i)
			}varu=window.opera;if(!r&&document.attachEvent&&(!u||"[object Opera]"!==u.toString())){
				vars=R();r=s&&s.getAttribute("data-require-id")
			}r?(a(r,
			n,
			t),
			H&&clearTimeout(H),
			H=setTimeout(o,
			1)): rr.push({
				deps: n,
				factory: t
			})
		}
	}functioni(){
		vare=tr.config[this.id];returne&&"object"==typeofe?e: {
			
		}
	}functiona(e,
	r,
	n){
		if(!F[e]){
			vart={
				id: e,
				deps: r||["require",
				"exports",
				"module"],
				factoryDeps: [],
				factory: n,
				exports: {
					
				},
				config: i,
				state: P,
				require: k(e),
				depMs: [],
				depMsIndex: {
					
				},
				depRs: [],
				depPMs: {
					
				}
			};F[e]=t,
			_.push(t)
		}
	}functiono(){
		functione(e){
			F[e]||n[e]||(r.push(e),
			n[e]=1)
		}varr=[],
		n={
			
		};A(_,
		function(r){
			if(!(r.state>P)){
				varn=r.deps.slice(0),
				t=n.length,
				i=0,
				a=r.factory;"function"==typeofa&&(i=Math.min(a.length,
				t),
				a.toString().replace(G,
				"").replace(Q,
				function(e,
				r,
				t){
					n.push(t)
				})),
				A(n,
				function(n,
				a){
					varo,
					u,
					s=U(n),
					c=E(s.module,
					r.id);c&&!er[c]?(s.resource&&(u={
						id: n,
						module: c,
						resource: s.resource
					},
					r.depPMs[c]=1,
					r.depRs.push(u)),
					o=r.depMsIndex[c],
					o||(o={
						id: s.module,
						absId: c,
						hard: i>a,
						circular: W
					},
					r.depMs.push(o),
					r.depMsIndex[c]=o,
					e(c))): o={
						absId: c
					},
					t>a&&r.factoryDeps.push(u||o)
				}),
				r.state=B,
				A(r.depMs,
				function(e){
					u(r.id,
					e.absId)
				}),
				s(r)
			}
		}),
		b(r)
	}functionu(e,
	r){
		functionn(){
			p(e)
		}g(r,
		function(){
			vart=F[e];t.depPMs[r]&&A(t.depRs,
			function(t){
				t.absId||t.module!==r||(t.absId=E(t.id,
				e),
				g(t.absId,
				n),
				b([t.absId],
				null,
				e))
			}),
			n()
		})
	}functions(r){
		functionn(){
			vare=V;returnA(r.depRs,
			function(r){
				returnr.absId&&f(r.absId)?void0: (e=J,
				!1)
			}),
			e!==V?e: (A(r.depMs,
			function(r){
				if(!f(r.absId))switch(r.circular===W&&(r.circular=l(a,
				r.absId)),
				r.circular){
					caseY: r.hard&&(e=K);break;caseX: e=K;break;caseW: returne=J,
					!1
				}
			}),
			e)
		}functiont(){
			if(!(r.state>=L)){
				vart=n();if(t>=K&&i(),
				!(V>t)){
					varo=[];A(r.factoryDeps,
					function(e){
						o.push(e.absId)
					});varu=v(o,
					{
						require: r.require,
						exports: r.exports,
						module: r
					});try{
						vars=r.factory,
						c="function"==typeofs?s.apply(e,
						u): s;null!=c&&(r.exports=c)
					}catch(f){
						if(/^\[MODULE_MISS\]"([^"]+)/.test(f.message)){
							vard=r.depMsIndex[RegExp.$1];returnd&&(d.hard=1),
							void0
						}throwf
					}r.state=L,
					r.invokeFactory=null,
					h(a)
				}
			}
		}functioni(){
			o||(o=1,
			A(r.depMs,
			function(e){
				e.circular===Y&&p(e.absId)
			}))
		}vara=r.id;r.invokeFactory=t,
		t();varo
	}functionc(e){
		returnF[e]&&F[e].state>=B
	}functionf(e){
		returnF[e]&&F[e].state>=L
	}functiond(e,
	r){
		varn=F[e];if(r=r||{
			
		},
		r[e]=1,
		!n||n.state<L)return!1;if(n.state===N)return!0;for(vart=n.depMs,
		i=t.length;i--;){
			vara=t[i].absId;if(!r[a]&&!d(a,
			r))return!1
		}returnn.state=N,
		!0
	}functionv(e,
	r){
		varn=[];returnA(e,
		function(e){
			n.push(r[e]||m(e))
		}),
		n
	}functionl(e,
	r,
	n){
		if(!c(r))returnW;n=n||{
			
		},
		n[r]=1;vart=F[r];if(r===e)returnY;vari=t&&t.depMs;if(i)for(vara=i.length;a--;){
			varo=i[a].absId;if(!n[o]){
				varu=l(e,
				o,
				n);switch(u){
					caseY: caseW: returnu
				}
			}
		}returnX
	}functionp(e){
		varr=F[e];r&&r.invokeFactory&&r.invokeFactory()
	}functionh(e){
		for(varr=Z[e]||[],
		n=r.length;n--;){
			vart=r[n];t&&t()
		}r.length=0,
		deleteZ[e]
	}functiong(e,
	r,
	n){
		if(f(e))returnr(e),
		void0;vart=Z[e];t||(t=Z[e]=[]),
		n?t.unshift(r): t.push(r)
	}functionm(e){
		returnf(e)?F[e].exports: null
	}functiony(e){
		varr=rr.slice(0);rr.length=0,
		rr=[],
		A(r,
		function(r){
			a(r.id||e,
			r.deps,
			r.factory)
		}),
		o()
	}functionb(r,
	n,
	t){
		functioni(){
			if(!a){
				vart=1;A(r,
				function(e){
					returner[e]?void0: t=d(e)
				}),
				t&&(a=1,
				"function"==typeofn&&n.apply(e,
				v(r,
				er)))
			}
		}if("string"==typeofr){
			if(!f(r))thrownewError('[MODULE_MISS]"'+r+'"isnotexists!');returnm(r)
		}vara=0;j(r)&&(i(),
		!a&&A(r,
		function(e){
			er[e]||(g(e,
			i,
			1),
			(e.indexOf("!")>0?M: I)(e,
			t))
		}))
	}functionI(e){
		functionr(){
			varr=n.readyState;("undefined"==typeofr||/^(loaded|complete)$/.test(r))&&(n.onload=n.onreadystatechange=null,
			n=null,
			y(e))
		}if(!nr[e]&&!F[e]){
			nr[e]=1;varn=document.createElement("script");n.setAttribute("data-require-id",
			e),
			n.src=w(e+".js"),
			n.async=!0,
			n.readyState?n.onreadystatechange=r: n.onload=r,
			T(n)
		}
	}functionM(e,
	r){
		functionn(r){
			o.state=N,
			o.exports=r||!0,
			h(e)
		}functiont(t){
			varo=r?F[r].require: C;t.load(a.resource,
			o,
			n,
			i.call({
				id: e
			}))
		}if(!F[e]){
			vara=U(e),
			o={
				id: e,
				state: B
			};F[e]=o,
			n.fromText=function(e,
			r){
				newFunction(r)(),
				y(e)
			},
			b([a.module],
			t)
		}
	}functionx(){
		tr.baseUrl=tr.baseUrl.replace(/\/$/,
		"")+"/";vare=D();ir=O(tr.paths),
		ir.sort(e),
		or=O(tr.map),
		or.sort(e),
		A(or,
		function(r){
			varn=r.k;r.v=O(r.v),
			r.v.sort(e),
			r.reg="*"===n?/^/: $(n)
		}),
		ar=[],
		A(tr.packages,
		function(e){
			varr=e;"string"==typeofe&&(r={
				name: e.split("/")[0],
				location: e,
				main: "main"
			}),
			r.location=r.location||r.name,
			r.main=(r.main||"main").replace(/\.js$/i,
			""),
			ar.push(r)
		}),
		ar.sort(D("name")),
		sr=O(tr.urlArgs),
		sr.sort(e)
	}functionw(e){
		functionr(e){
			c||(s+=(s.indexOf("?")>0?"&": "?")+e,
			c=1)
		}varn=/(\.[a-z0-9]+)$/i,
		t=/(\?[^#]*)$/,
		i="",
		a=e,
		o="";t.test(e)&&(o=RegExp.$1,
		e=e.replace(t,
		"")),
		n.test(e)&&(i=RegExp.$1,
		a=e.replace(n,
		""));varu,
		s=a;A(ir,
		function(e){
			varr=e.k;return$(r).test(a)?(s=s.replace(r,
			e.v),
			u=1,
			!1): void0
		}),
		u||A(ar,
		function(e){
			varr=e.name;return$(r).test(a)?(s=s.replace(r,
			e.location),
			!1): void0
		}),
		/^([a-z]{
			2,
			10
		}: \/)?\//i.test(s)||(s=tr.baseUrl+s),
		s+=i+o;varc;returnA(sr,
		function(e){
			return$(e.k).test(a)?(r(e.v),
			!1): void0
		}),
		ur&&r(ur),
		s
	}functionk(e){
		functionr(r,
		t){
			if("string"==typeofr){
				vari=n[r];returni||(i=n[r]=b(E(r,
				e))),
				i
			}if(j(r)){
				vara=[];A(r,
				function(r){
					varn=U(r);n.resource&&a.push(E(n.module,
					e))
				}),
				b(a,
				function(){
					varn=[];A(r,
					function(r){
						n.push(E(r,
						e))
					}),
					b(n,
					t,
					e)
				},
				e)
			}
		}varn={
			
		};returnr.toUrl=function(r){
			returnw(E(r,
			e))
		},
		r
	}functionE(e,
	r){
		if(!e)return"";r=r||"";varn=U(e);if(!n)returne;vart=n.resource,
		i=S(n.module,
		r);if(A(ar,
		function(e){
			varr=e.name;returnr===i?(i=r+"/"+e.main,
			!1): void0
		}),
		A(or,
		function(e){
			returne.reg.test(r)?(A(e.v,
			function(e){
				varr=e.k,
				n=$(r);returnn.test(i)?(i=i.replace(r,
				e.v),
				!1): void0
			}),
			!1): void0
		}),
		t){
			vara=m(i);t=a.normalize?a.normalize(t,
			function(e){
				returnE(e,
				r)
			}): E(t,
			r),
			i+="!"+t
		}returni
	}functionS(e,
	r){
		if(0===e.indexOf(".")){
			varn=r.split("/"),
			t=e.split("/"),
			i=n.length-1,
			a=t.length,
			o=0,
			u=0;e: for(vars=0;a>s;s++){
				varc=t[s];switch(c){
					case"..": if(!(i>o))breake;o++,
					u++;break;case".": u++;break;default: breake
				}
			}returnn.length=i-o,
			t=t.slice(u),
			n.concat(t).join("/")
		}returne
	}functionq(e){
		functionr(e){
			0===e.indexOf(".")&&n.push(e)
		}varn=[];if("string"==typeofe?r(e): A(e,
		function(e){
			r(e)
		}),
		n.length>0)thrownewError("[REQUIRE_FATAL]Relative ID is not allowed in global require: "+n.join(", "))
	}functionU(e){
		varr=e.split("!");returndr.test(r[0])?{
			module: r[0],
			resource: r[1]
		}: null
	}functionO(e){
		varr=[];for(varnine)e.hasOwnProperty(n)&&r.push({
			k: n,
			v: e[n]
		});returnr
	}functionR(){
		if(cr)returncr;if(fr&&"interactive"===fr.readyState)returnfr;for(vare=document.getElementsByTagName("script"),
		r=e.length;r--;){
			varn=e[r];if("interactive"===n.readyState)returnfr=n,
			n
		}
	}functionT(e){
		cr=e,
		lr?vr.insertBefore(e,
		lr): vr.appendChild(e),
		cr=null
	}function$(e){
		returnnewRegExp("^"+e+"(/|$)")
	}functionj(e){
		returneinstanceofArray
	}functionA(e,
	r){
		if(j(e))for(varn=0,
		t=e.length;t>n&&r(e[n],
		n)!==!1;n++);
	}functionD(e){
		returne=e||"k",
		function(r,
		n){
			vart=r[e],
			i=n[e];return"*"===i?-1: "*"===t?1: i.length-t.length
		}
	}varz,
	F={
		
	},
	_=[],
	P=1,
	B=2,
	L=3,
	N=4,
	C=k();r.toUrl=C.toUrl;varH;t.amd={
		
	};varQ=/require\(\s*(['"'])([^'"]+)\1\s*\)/g,
	G=/(\/\*([\s\S]*?)\*\/|([^: ]|^)\/\/(.*)$)/gm,
	J=0,
	K=1,
	V=2,
	W=0,
	X=1,
	Y=2,
	Z={
		
	},
	er={
		require: r,
		exports: 1,
		module: 1
	},
	rr=[],
	nr={
		
	},
	tr={
		baseUrl: "./",
		paths: {
			
		},
		config: {
			
		},
		map: {
			
		},
		packages: [],
		waitSeconds: 0,
		urlArgs: {
			
		}
	};r.config=function(e){
		for(varrintr)if(e.hasOwnProperty(r)){
			varn=e[r],
			t=tr[r];if("urlArgs"===r&&"string"==typeofn)ur=n;else{
				vari=typeoft;if("string"===i||"number"===i)tr[r]=n;elseif(j(t))A(n,
				function(e){
					t.push(e)
				});elsefor(varrinn)t[r]=n[r]
			}
		}x()
	},
	x();varir,
	ar,
	or,
	ur,
	sr,
	cr,
	fr,
	dr=/^[-_a-z0-9\.]+(\/[-_a-z0-9\.]+)*$/i,
	vr=document.getElementsByTagName("head")[0],
	lr=document.getElementsByTagName("base")[0];lr&&(vr=lr.parentNode),
	e.define=t,
	e.require=r
}(this);