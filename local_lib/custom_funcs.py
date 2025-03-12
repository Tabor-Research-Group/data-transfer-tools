
import GPyOpt
import numpy as np
from Psience.Molecools import Molecule

def get_energy_func(mol:Molecule, evaluator=None, use_internals=True, reoptimize=True):
    def objective_func(coords):
        disp_coords = mol.get_displaced_coordinates(
            coords,
            use_internals=use_internals,
            shift=False
        )
        if reoptimize:
            return np.ndarray([
                mol.modify(coords=c)
                .optimize(evaluator=evaluator)
                .calculate_energy(evaluator=evaluator)
                for c in disp_coords
                ])
        else:
            return mol.calculate_energy(disp_coords)

    return objective_func

def get_optimizer(
        mol_spec,
        *,
        domain,
        internals=None,
        acquisition_type='EI',
        constraints=None,
        exact_feval=False,
        evaluator_type='random',
        batch_size=1,
        **opts
):
    mol = Molecule.construct(mol_spec,
                             internals=internals,
                             **opts
                             )
    return GPyOpt.methods.BayesianOptimization(
        f=get_energy_func(mol, use_internals=True),
        domain=domain,
        acquisition_type=acquisition_type,
        initial_design_numdata=batch_size,
        evaluator_type=evaluator_type,
        exact_feval=exact_feval,
        constraints=constraints
    )


def optimize_system(
        mol_spec,
        *,
        max_iter=100,
        log_file=None,
        **opts
):
    optimizer = get_optimizer(mol_spec, **opts)
    optimizer.run_optimization(max_iter=max_iter)
    if log_file is not None:
        optimizer.save_report(log_file)

    return optimizer
