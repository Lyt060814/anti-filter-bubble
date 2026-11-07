from experiments import *

ARMS = ['S0','S1a','S1b','S2','S3','S4','S5','S6','S7','S8','S9']


def escape():
    rows, persistence = [], []
    for ratio in RATIOS:
        for seed in SEEDS:
            model, endpoints, ahist, ref, _ = population(ratio, seed)
            for q, theta in enumerate(THETAS):
                # Coupled random numbers across arms reduce comparison variance.
                rng = np.random.default_rng(10000+100*seed+q)
                u = np.tile(endpoints[q], (len(ARMS), 1))
                u[6] -= ahist[q]  # delete surviving contributions from A once
                u[10] = 0       # reset once, not every exposure
                basepi = model.probabilities(endpoints[q])
                bm, bp, bv = model.metrics(basepi, ref)
                bmass = basepi[model.B].sum()
                effort = np.zeros(len(ARMS))
                effort[6] = 1  # one bulk-delete action
                effort[10] = 1
                trajectory = []
                for step in range(ACTIVE+FOLLOW+1):
                    active = step <= ACTIVE
                    serving = u.copy()
                    if active:
                        serving[9] = endpoints.mean(axis=0)  # task specifies mean u
                    logits = serving @ model.v.T / model.cfg.tau
                    logits -= logits.max(axis=1, keepdims=True)
                    pi = np.exp(logits)
                    pi /= pi.sum(axis=1, keepdims=True)
                    rejection = 0.
                    if active:
                        rejection = .8*pi[7, model.A].sum()+.02*pi[7, model.B].sum()
                        pi[7, model.A] *= .2
                        pi[7, model.B] *= .98
                        pi[7] /= pi[7].sum()  # refill from remaining catalogue
                        pi[8, model.I] = 0
                        pi[8] /= pi[8].sum()
                    ms = pi[:, model.I].sum(axis=1)
                    aa = pi[:, model.A].sum(axis=1)
                    bb = pi[:, model.B].sum(axis=1)
                    vs = np.full(len(ARMS), np.nan)
                    valid = (aa > 0) & (bb > 0)
                    vs[valid] = np.log(aa[valid]/bb[valid])-reference_logit(ref)
                    trajectory.append(vs.copy())
                    if step % 20 == 0 or step == ACTIVE+1:
                        for arm, name in enumerate(ARMS):
                            rows.append(dict(ratio=ratio, theta=theta, seed=seed, strategy=name,
                                step=step, active=active, m=ms[arm], V=vs[arm],
                                delta_V=vs[arm]-bv,
                                delta_log_m=np.log(ms[arm]/bm) if ms[arm]>0 else -np.inf,
                                B_retention=bb[arm]/bmass, effort=effort[arm],
                                delta_V_vs_control=vs[arm]-vs[0], reference=ref[0]/sum(ref)))
                    if step == ACTIVE+FOLLOW:
                        break
                    if step == ACTIVE:
                        # Endpoint reports the still-enabled intervention.
                        # Remove output controls BEFORE the next natural draw.
                        logits = u @ model.v.T / model.cfg.tau
                        logits -= logits.max(axis=1, keepdims=True)
                        pi = np.exp(logits)
                        pi /= pi.sum(axis=1, keepdims=True)
                    uniform, completion, search = rng.random(3)
                    j = (np.cumsum(pi, axis=1) < uniform).sum(axis=1)
                    prob = 1/(1+np.exp(-(-1+model.I[j]+theta*model.A[j])))
                    coef = (completion < prob).astype(float)
                    if step < ACTIVE:
                        if model.A[j[1]]:
                            coef[1] = -1
                            effort[1] += 1
                        if model.A[j[2]]:
                            coef[2] = .5
                            effort[2] += 1
                        if model.A[j[3]]:
                            coef[3] = 0
                            effort[3] += 1
                        if model.B[j[4]]:
                            coef[4] = 1
                            effort[4] += 1
                        effort[7] += rejection  # expected per-slot rejected mass
                        if step == 0:
                            effort[7:10] += 1  # enable filter, topic-off, mean-u
                    u = (1-model.cfg.decay)*u+model.cfg.eta*coef[:,None]*model.v[j]
                    if step < ACTIVE and step % 10 == 0:
                        u[5] += model.cfg.eta*model.v[40+min(39,int(search*40))]
                        effort[5] += 1
                trajectory = np.array(trajectory)
                for arm, name in enumerate(ARMS):
                    reduction = bv-trajectory[ACTIVE,arm]
                    after = bv-trajectory[ACTIVE+1:,arm]
                    hit = np.where(after <= reduction/2)[0] if reduction>0 else []
                    relative = trajectory[ACTIVE,0]-trajectory[ACTIVE,arm]
                    relative_after = trajectory[ACTIVE+1:,0]-trajectory[ACTIVE+1:,arm]
                    rhit = np.where(relative_after <= relative/2)[0] if relative>0 else []
                    persistence.append(dict(ratio=ratio,theta=theta,seed=seed,strategy=name,
                        reduction=reduction, half_life=(int(hit[0])+1) if len(hit) else np.nan,
                        censored=bool(reduction>0 and not len(hit)),
                        control_reduction=relative,
                        control_half_life=(int(rhit[0])+1) if len(rhit) else np.nan,
                        control_censored=bool(relative>0 and not len(rhit)), horizon=FOLLOW))
        print(f'R3 c/t={ratio}: 4 theta x 20 seeds x 11 arms complete', flush=True)
    save_csv('escape', rows)
    save_csv('persistence', persistence)
    plot_escape(rows)


def plot_escape(rows):
    fig, axes = plt.subplots(2,2,figsize=(12,9))
    for ax, ratio in zip(axes[0],(.15,.59)):
        for index,name in enumerate(ARMS):
            group = [r for r in rows if r['ratio']==ratio and r['theta']==2 and r['strategy']==name and r['step']==ACTIVE]
            if name == 'S7':
                continue  # zero topic: V undefined, log m = -infinity
            x, ex = ci([r['delta_log_m'] for r in group])
            y, ey = ci([r['delta_V'] for r in group])
            ax.errorbar(x,y,xerr=ex,yerr=ey,fmt='o',color=plt.cm.tab20(index/20),label=name)
        ax.axhline(0,color='grey',lw=.5)
        ax.axvline(0,color='grey',lw=.5)
        ax.set(title=f'theta=2; c/t={ratio}; S7 undefined (m=0)', xlabel='Change in log topic exposure', ylabel='Change in personal skew V')
        ax.text(.03,.03,'Desired: lower V near vertical x=0 line',transform=ax.transAxes,fontsize=8)
        ax.margins(x=.12,y=.12)
        ax.legend(fontsize=7,ncol=2,loc='center left')
    for ax, field in zip(axes[1],('delta_V','delta_log_m')):
        for index, name in enumerate(ARMS):
            if name=='S7':
                continue
            means, errors = [], []
            for ratio in RATIOS:
                group = [r[field] for r in rows if r['ratio']==ratio and r['theta']==2 and r['strategy']==name and r['step']==ACTIVE]
                mean, error = ci(group)
                means.append(mean)
                errors.append(error)
            means, errors = np.array(means),np.array(errors)
            line, = ax.plot(RATIOS,means,label=name,color=plt.cm.tab20(index/20))
            ax.fill_between(RATIOS,means-errors,means+errors,color=line.get_color(),alpha=.08)
        ax.axhline(0,color='grey',lw=.5)
        ax.set(xlabel='Generating coefficient c/t',ylabel=field,title='theta=2; full coefficient scan')
    axes[1,1].legend(fontsize=7,ncol=3)
    figure('escape',dict(script='analysis/v6_simulation/escape.py', classifier_assumption=dict(TPR=.8,FPR=.02), negative_NI_multiplier=-1,
                         reverse_NI_multiplier=.5, search_every=10, reset_and_delete='once at start',
                         reference='frozen R2 terminal population mean exposure',
                         S8='softmax(mean user vector); not mean softmax probabilities; V need not equal zero',
                         filtration='expected class-dependent thinning with refill; outside unaffected',
                         effort='actions; S6 also records expected rejected mass, not human effort'))
    fig, axes = plt.subplots(1,2,figsize=(12,5))
    for ax, ratio in zip(axes,(.15,.59)):
        for index,name in enumerate(ARMS):
            group = [r for r in rows if r['ratio']==ratio and r['theta']==2 and r['strategy']==name and r['step']>=ACTIVE]
            vals = np.array([r['delta_V_vs_control'] for r in group]).reshape(20,-1)
            mean, error = ci(vals)
            steps = sorted(set(r['step']-ACTIVE for r in group))
            line, = ax.plot(steps, mean, label=name,color=plt.cm.tab20(index/20))
            ax.fill_between(steps,mean-error,mean+error,alpha=.08,color=line.get_color())
        ax.axvline(1,color='grey',linestyle='--')
        ax.set(title=f'theta=2; c/t={ratio}; removal at step +1',xlabel='Exposures after active endpoint',ylabel='V difference from matched S0')
    axes[1].legend(fontsize=7,ncol=2)
    figure('persistence',dict(script='analysis/v6_simulation/escape.py', extra_csv='escape.csv', followup_right_censoring=FOLLOW,
                             half_life='task: rebound toward pre-intervention V; also matched-S0 half-life recorded'))


if __name__ == '__main__':
    escape()
