########################################################################################################################
# Copyright © 2019 The George Washington University.
# All Rights Reserved.
#
# Contributors: Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Licensed under the BSD-3-Clause License (the "License").
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at: https://opensource.org/licenses/BSD-3-Clause
#
# BSD-3-Clause License:
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided
# that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
#    following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or
#    promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
########################################################################################################################
from __future__ import absolute_import
from __future__ import print_function
import os
import numpy
def setrun(claw_pkg='geoclaw'):
    from clawpack.clawutil import data
    assert claw_pkg.lower() == 'geoclaw',  'Expected claw_pkg = geoclaw'
    num_dim = 2
    rundata = data.ClawRunData(claw_pkg, num_dim)
    rundata.add_attribute('topo_source', '3DEP')
    rundata.add_attribute('username', 'None')
    rundata.add_attribute('passcode', None)
    rundata = setgeo(rundata)
    rundata = setamr(rundata)
    clawdata = rundata.clawdata
    clawdata.num_dim = num_dim
    clawdata.lower[0] = -9964905.4944-1998.0
    clawdata.upper[0] = -9964905.4944+1998.0
    clawdata.lower[1] = 3717211.577799998-1998.0
    clawdata.upper[1] = 3717211.577799998+1998.0
    clawdata.num_cells[0] = 333
    clawdata.num_cells[1] = 333
    clawdata.num_eqn = 3
    clawdata.num_aux = 2
    clawdata.capa_index = 0
    clawdata.t0 = 0.0
    clawdata.restart = False
    clawdata.restart_file = 'fort.chk00006'
    clawdata.output_style = 2
    clawdata.output_times = list(numpy.arange(0, 43200.0+1, 120.0))
    clawdata.output_format = 'binary'
    clawdata.output_q_components = 'all'
    clawdata.output_aux_components = 'all'
    clawdata.output_aux_onlyonce = True
    clawdata.verbosity = 2
    clawdata.dt_variable = 1
    clawdata.dt_max = 4.0
    clawdata.dt_initial = 1.0
    clawdata.cfl_desired = 0.9
    clawdata.cfl_max = 0.95
    clawdata.steps_max = 100000
    clawdata.order = 2
    clawdata.dimensional_split = 'unsplit'
    clawdata.transverse_waves = 2
    clawdata.num_waves = 3
    clawdata.limiter = ['mc', 'mc', 'mc']
    clawdata.use_fwaves = True
    clawdata.source_split = 'godunov'
    clawdata.num_ghost = 2
    clawdata.bc_lower[0] = 1
    clawdata.bc_upper[0] = 1
    clawdata.bc_lower[1] = 1
    clawdata.bc_upper[1] = 1
    clawdata.checkpt_style = 0
    return rundata
def setamr(rundata):
    try:
        amrdata = rundata.amrdata
    except:
        print('*** Error, this rundata has no amrdata attribute')
        raise AttributeError('Missing amrdata attribute')
    amrdata.amr_levels_max = 2
    amrdata.refinement_ratios_x = [4]
    amrdata.refinement_ratios_y = [4]
    amrdata.refinement_ratios_t = [4]
    amrdata.aux_type = ['center', 'center']
    amrdata.flag_richardson = False
    amrdata.flag2refine = True
    amrdata.regrid_interval = 1
    amrdata.regrid_buffer_width  = 1
    amrdata.clustering_cutoff = 0.80000
    amrdata.verbosity_regrid = 0
    amrdata.dprint = False
    amrdata.eprint = False
    amrdata.edebug = False
    amrdata.gprint = False
    amrdata.nprint = False
    amrdata.pprint = False
    amrdata.rprint = False
    amrdata.sprint = False
    amrdata.tprint = False
    amrdata.uprint = False
    regions = rundata.regiondata.regions
    return rundata
def setgeo(rundata):
    try:
        geo_data = rundata.geo_data
    except:
        print('*** Error, this rundata has no geo_data attribute')
        raise AttributeError('Missing geo_data attribute')
    geo_data.gravity = 9.81
    geo_data.coordinate_system = 1
    geo_data.earth_radius = 6367.5e3
    geo_data.coriolis_forcing = False
    geo_data.sea_level = -100.0
    geo_data.dry_tolerance = 1.e-4
    geo_data.friction_forcing = False
    geo_data.manning_coefficient = 0.035
    geo_data.friction_depth = 1.e6
    geo_data.update_tol = geo_data.dry_tolerance
    geo_data.refine_tol = 0.0
    refinement_data = rundata.refinement_data
    refinement_data.wave_tolerance = 1.e-5
    refinement_data.speed_tolerance = [1e-8]
    refinement_data.deep_depth = 1e2
    refinement_data.max_level_deep = 3
    refinement_data.variable_dt_refinement_ratios = True
    topo_data = rundata.topo_data
    topo_data.topofiles.append([3, 1, 5, 0., 1.e10, "topo.asc"])
    dtopo_data = rundata.dtopo_data
    rundata.qinit_data.qinit_type = 0
    rundata.qinit_data.qinitfiles = []
    fixedgrids = rundata.fixed_grid_data
    from clawpack.geoclaw.data import LandSpillData
    rundata.add_data(LandSpillData(), 'landspill_data')
    landspill = rundata.landspill_data
    landspill.ref_mu = 0.7977962683529538
    landspill.ref_temperature = 40.0
    landspill.ambient_temperature = 15.5
    landspill.density = 746.0
    ptsources_data = landspill.point_sources
    ptsources_data.n_point_sources = 8
    ptsources_data.point_sources.append([[-9964905.4944, 3717231.577799998], 1,  [120.00000796247471], [9.983543586844673]])
    ptsources_data.point_sources.append([[-9964891.3523, 3717225.719899997], 1,  [120.00000796247471], [9.983543586844673]])
    ptsources_data.point_sources.append([[-9964885.4944, 3717211.577799998], 1,  [120.00000796247471], [9.983543586844673]])
    ptsources_data.point_sources.append([[-9964891.3523, 3717197.4356999993], 1,  [120.00000796247471], [9.983543586844673]])
    ptsources_data.point_sources.append([[-9964905.4944, 3717191.577799998], 1,  [120.00000796247471], [9.983543586844673]])
    ptsources_data.point_sources.append([[-9964919.6365, 3717197.4356999993], 1,  [120.00000796247471], [9.983543586844673]])
    ptsources_data.point_sources.append([[-9964925.4944, 3717211.577799998], 1,  [120.00000796247471], [9.983543586844673]])
    ptsources_data.point_sources.append([[-9964919.6365, 3717225.719899997], 1,  [120.00000796247471], [9.983543586844673]])
    darcy_weisbach_data = landspill.darcy_weisbach_friction
    darcy_weisbach_data.type = 4
    darcy_weisbach_data.dry_tol = 1e-4
    darcy_weisbach_data.friction_tol = 1e6
    darcy_weisbach_data.default_roughness = 0.1
    darcy_weisbach_data.filename = 'roughness.txt'
    hydro_feature_data = landspill.hydro_features
    hydro_feature_data.files = ['hydro_0.asc']
    evaporation_data = landspill.evaporation
    evaporation_data.type = 1
    evaporation_data.coefficients = [6.754607, 0.045   ]
    return rundata
if __name__ == '__main__':
    import sys
    rundata = setrun(*sys.argv[1:])
    rundata.write()