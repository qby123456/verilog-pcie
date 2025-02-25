"""

Copyright (c) 2020 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import logging
import os

import cocotb_test.simulator

import cocotb
from cocotb.log import SimLog
from cocotb.triggers import RisingEdge, FallingEdge, Timer

from cocotbext.axi import AxiStreamBus
from cocotbext.pcie.core import RootComplex
from cocotbext.pcie.xilinx.us import UltraScalePcieDevice


class TB(object):
    def __init__(self, dut):
        self.dut = dut

        self.log = SimLog("cocotb.tb")
        self.log.setLevel(logging.DEBUG)

        # PCIe
        self.rc = RootComplex()

        self.dev = UltraScalePcieDevice(
            # configuration options
            pcie_generation=3,
            pcie_link_width=8,
            user_clk_frequency=250e6,
            alignment="dword",
            rc_straddle=True,
            pf_count=1,
            max_payload_size=1024,
            enable_client_tag=True,
            enable_extended_tag=True,
            enable_parity=False,
            enable_rx_msg_interface=False,
            enable_sriov=False,
            enable_extended_configuration=False,

            pf0_msi_enable=False,
            pf0_msi_count=1,
            pf1_msi_enable=False,
            pf1_msi_count=1,
            pf0_msix_enable=True,
            pf0_msix_table_size=31,
            pf0_msix_table_bir=4,
            pf0_msix_table_offset=0x00000000,
            pf0_msix_pba_bir=4,
            pf0_msix_pba_offset=0x00008000,
            pf1_msix_enable=False,
            pf1_msix_table_size=0,
            pf1_msix_table_bir=0,
            pf1_msix_table_offset=0x00000000,
            pf1_msix_pba_bir=0,
            pf1_msix_pba_offset=0x00000000,

            # signals
            # Clock and Reset Interface
            user_clk=dut.clk,
            user_reset=dut.rst,
            # user_lnk_up
            # sys_clk
            # sys_clk_gt
            # sys_reset
            # phy_rdy_out

            # Requester reQuest Interface
            rq_bus=AxiStreamBus.from_prefix(dut, "m_axis_rq"),
            pcie_rq_seq_num=dut.s_axis_rq_seq_num,
            pcie_rq_seq_num_vld=dut.s_axis_rq_seq_num_valid,
            # pcie_rq_tag
            # pcie_rq_tag_av
            # pcie_rq_tag_vld

            # Requester Completion Interface
            rc_bus=AxiStreamBus.from_prefix(dut, "s_axis_rc"),

            # Completer reQuest Interface
            cq_bus=AxiStreamBus.from_prefix(dut, "s_axis_cq"),
            # pcie_cq_np_req
            # pcie_cq_np_req_count

            # Completer Completion Interface
            cc_bus=AxiStreamBus.from_prefix(dut, "m_axis_cc"),

            # Transmit Flow Control Interface
            # pcie_tfc_nph_av=dut.pcie_tfc_nph_av,
            # pcie_tfc_npd_av=dut.pcie_tfc_npd_av,

            # Configuration Management Interface
            cfg_mgmt_addr=dut.cfg_mgmt_addr,
            cfg_mgmt_write=dut.cfg_mgmt_write,
            cfg_mgmt_write_data=dut.cfg_mgmt_write_data,
            cfg_mgmt_byte_enable=dut.cfg_mgmt_byte_enable,
            cfg_mgmt_read=dut.cfg_mgmt_read,
            cfg_mgmt_read_data=dut.cfg_mgmt_read_data,
            cfg_mgmt_read_write_done=dut.cfg_mgmt_read_write_done,
            # cfg_mgmt_debug_access

            # Configuration Status Interface
            # cfg_phy_link_down
            # cfg_phy_link_status
            # cfg_negotiated_width
            # cfg_current_speed
            cfg_max_payload=dut.cfg_max_payload,
            cfg_max_read_req=dut.cfg_max_read_req,
            # cfg_function_status
            # cfg_vf_status
            # cfg_function_power_state
            # cfg_vf_power_state
            # cfg_link_power_state
            # cfg_err_cor_out
            # cfg_err_nonfatal_out
            # cfg_err_fatal_out
            # cfg_local_error_out
            # cfg_local_error_valid
            # cfg_rx_pm_state
            # cfg_tx_pm_state
            # cfg_ltssm_state
            # cfg_rcb_status
            # cfg_obff_enable
            # cfg_pl_status_change
            # cfg_tph_requester_enable
            # cfg_tph_st_mode
            # cfg_vf_tph_requester_enable
            # cfg_vf_tph_st_mode

            # Configuration Received Message Interface
            # cfg_msg_received
            # cfg_msg_received_data
            # cfg_msg_received_type

            # Configuration Transmit Message Interface
            # cfg_msg_transmit
            # cfg_msg_transmit_type
            # cfg_msg_transmit_data
            # cfg_msg_transmit_done

            # Configuration Flow Control Interface
            cfg_fc_ph=dut.cfg_fc_ph,
            cfg_fc_pd=dut.cfg_fc_pd,
            cfg_fc_nph=dut.cfg_fc_nph,
            cfg_fc_npd=dut.cfg_fc_npd,
            cfg_fc_cplh=dut.cfg_fc_cplh,
            cfg_fc_cpld=dut.cfg_fc_cpld,
            cfg_fc_sel=dut.cfg_fc_sel,

            # Configuration Control Interface
            # cfg_hot_reset_in
            # cfg_hot_reset_out
            # cfg_config_space_enable
            # cfg_dsn
            # cfg_bus_number
            # cfg_ds_port_number
            # cfg_ds_bus_number
            # cfg_ds_device_number
            # cfg_ds_function_number
            # cfg_power_state_change_ack
            # cfg_power_state_change_interrupt
            cfg_err_cor_in=dut.status_error_cor,
            cfg_err_uncor_in=dut.status_error_uncor,
            # cfg_flr_in_process
            # cfg_flr_done
            # cfg_vf_flr_in_process
            # cfg_vf_flr_func_num
            # cfg_vf_flr_done
            # cfg_pm_aspm_l1_entry_reject
            # cfg_pm_aspm_tx_l0s_entry_disable
            # cfg_req_pm_transition_l23_ready
            # cfg_link_training_enable

            # Configuration Interrupt Controller Interface
            # cfg_interrupt_int
            # cfg_interrupt_sent
            # cfg_interrupt_pending
            # cfg_interrupt_msi_enable
            # cfg_interrupt_msi_vf_enable
            # cfg_interrupt_msi_mmenable
            # cfg_interrupt_msi_mask_update
            # cfg_interrupt_msi_data
            # cfg_interrupt_msi_select
            # cfg_interrupt_msi_int
            # cfg_interrupt_msi_pending_status
            # cfg_interrupt_msi_pending_status_data_enable
            # cfg_interrupt_msi_pending_status_function_num
            # cfg_interrupt_msi_sent
            # cfg_interrupt_msi_fail
            cfg_interrupt_msix_enable=dut.cfg_interrupt_msix_enable,
            cfg_interrupt_msix_mask=dut.cfg_interrupt_msix_mask,
            cfg_interrupt_msix_vf_enable=dut.cfg_interrupt_msix_vf_enable,
            cfg_interrupt_msix_vf_mask=dut.cfg_interrupt_msix_vf_mask,
            cfg_interrupt_msix_address=dut.cfg_interrupt_msix_address,
            cfg_interrupt_msix_data=dut.cfg_interrupt_msix_data,
            cfg_interrupt_msix_int=dut.cfg_interrupt_msix_int,
            cfg_interrupt_msix_sent=dut.cfg_interrupt_msix_sent,
            cfg_interrupt_msix_fail=dut.cfg_interrupt_msix_fail,
            # cfg_interrupt_msi_attr
            # cfg_interrupt_msi_tph_present
            # cfg_interrupt_msi_tph_type
            # cfg_interrupt_msi_tph_st_tag
            cfg_interrupt_msi_function_number=dut.cfg_interrupt_msi_function_number,

            # Configuration Extend Interface
            # cfg_ext_read_received
            # cfg_ext_write_received
            # cfg_ext_register_number
            # cfg_ext_function_number
            # cfg_ext_write_data
            # cfg_ext_write_byte_enable
            # cfg_ext_read_data
            # cfg_ext_read_data_valid
        )

        # self.dev.log.setLevel(logging.DEBUG)

        self.rc.make_port().connect(self.dev)

        self.dev.functions[0].configure_bar(0, 2**len(dut.example_core_pcie_us_inst.core_pcie_inst.axil_ctrl_awaddr))
        self.dev.functions[0].configure_bar(2, 2**len(dut.example_core_pcie_us_inst.core_pcie_inst.axi_ram_awaddr))
        self.dev.functions[0].configure_bar(4, 2**len(dut.example_core_pcie_us_inst.core_pcie_inst.axil_msix_awaddr))

    async def init(self):

        await FallingEdge(self.dut.rst)
        await Timer(100, 'ns')

        await self.rc.enumerate()

        dev = self.rc.find_device(self.dev.functions[0].pcie_id)
        await dev.enable_device()
        await dev.set_master()
        await dev.alloc_irq_vectors(32, 32)


@cocotb.test()
async def run_test(dut):

    tb = TB(dut)

    await tb.init()

    mem = tb.rc.mem_pool.alloc_region(16*1024*1024)
    mem_base = mem.get_absolute_address(0)

    dev = tb.rc.find_device(tb.dev.functions[0].pcie_id)

    dev_pf0_bar0 = dev.bar_window[0]
    dev_pf0_bar2 = dev.bar_window[2]

    tb.log.info("Test memory write to BAR 2")

    test_data = b'\x11\x22\x33\x44'
    await dev_pf0_bar2.write(0, test_data)

    await Timer(100, 'ns')

    tb.log.info("Test memory read from BAR 2")

    val = await dev_pf0_bar2.read(0, len(test_data), timeout=1000)
    tb.log.info("Read data: %s", val)
    assert val == test_data

    tb.log.info("Test DMA")

    # write packet data
    mem[0:1024] = bytearray([x % 256 for x in range(1024)])

    # enable DMA
    await dev_pf0_bar0.write_dword(0x000000, 1)
    # enable interrupts
    await dev_pf0_bar0.write_dword(0x000008, 0x3)

    # write pcie read descriptor
    await dev_pf0_bar0.write_dword(0x000100, (mem_base+0x0000) & 0xffffffff)
    await dev_pf0_bar0.write_dword(0x000104, (mem_base+0x0000 >> 32) & 0xffffffff)
    await dev_pf0_bar0.write_dword(0x000108, 0x100)
    await dev_pf0_bar0.write_dword(0x000110, 0x400)
    await dev_pf0_bar0.write_dword(0x000114, 0xAA)

    await Timer(2000, 'ns')

    # read status
    val = await dev_pf0_bar0.read_dword(0x000118)
    tb.log.info("Status: 0x%x", val)
    assert val == 0x800000AA

    # write pcie write descriptor
    await dev_pf0_bar0.write_dword(0x000200, (mem_base+0x1000) & 0xffffffff)
    await dev_pf0_bar0.write_dword(0x000204, (mem_base+0x1000 >> 32) & 0xffffffff)
    await dev_pf0_bar0.write_dword(0x000208, 0x100)
    await dev_pf0_bar0.write_dword(0x000210, 0x400)
    await dev_pf0_bar0.write_dword(0x000214, 0x55)

    await Timer(2000, 'ns')

    # read status
    val = await dev_pf0_bar0.read_dword(0x000218)
    tb.log.info("Status: 0x%x", val)
    assert val == 0x80000055

    tb.log.info("%s", mem.hexdump_str(0x1000, 64))

    assert mem[0:1024] == mem[0x1000:0x1000+1024]

    tb.log.info("Test immediate write")

    # write pcie write descriptor
    await dev_pf0_bar0.write_dword(0x000200, (mem_base+0x1000) & 0xffffffff)
    await dev_pf0_bar0.write_dword(0x000204, (mem_base+0x1000 >> 32) & 0xffffffff)
    await dev_pf0_bar0.write_dword(0x000208, 0x44332211)
    await dev_pf0_bar0.write_dword(0x000210, 0x4)
    await dev_pf0_bar0.write_dword(0x000214, 0x800000AA)

    await Timer(2000, 'ns')

    # read status
    val = await dev_pf0_bar0.read_dword(0x000218)
    tb.log.info("Status: 0x%x", val)
    assert val == 0x800000AA

    tb.log.info("%s", mem.hexdump_str(0x1000, 64))

    assert mem[0x1000:0x1000+4] == b'\x11\x22\x33\x44'

    tb.log.info("Test DMA block operations")

    region_len = 0x2000
    src_offset = 0x0000
    dest_offset = 0x4000

    block_size = 256
    block_stride = block_size
    block_count = 32

    # write packet data
    mem[src_offset:src_offset+region_len] = bytearray([x % 256 for x in range(region_len)])

    # enable DMA
    await dev_pf0_bar0.write_dword(0x000000, 1)
    # disable interrupts
    await dev_pf0_bar0.write_dword(0x000008, 0)

    # configure operation (read)
    # DMA base address
    await dev_pf0_bar0.write_dword(0x001080, (mem_base+src_offset) & 0xffffffff)
    await dev_pf0_bar0.write_dword(0x001084, (mem_base+src_offset >> 32) & 0xffffffff)
    # DMA offset address
    await dev_pf0_bar0.write_dword(0x001088, 0)
    await dev_pf0_bar0.write_dword(0x00108c, 0)
    # DMA offset mask
    await dev_pf0_bar0.write_dword(0x001090, region_len-1)
    await dev_pf0_bar0.write_dword(0x001094, 0)
    # DMA stride
    await dev_pf0_bar0.write_dword(0x001098, block_stride)
    await dev_pf0_bar0.write_dword(0x00109c, 0)
    # RAM base address
    await dev_pf0_bar0.write_dword(0x0010c0, 0)
    await dev_pf0_bar0.write_dword(0x0010c4, 0)
    # RAM offset address
    await dev_pf0_bar0.write_dword(0x0010c8, 0)
    await dev_pf0_bar0.write_dword(0x0010cc, 0)
    # RAM offset mask
    await dev_pf0_bar0.write_dword(0x0010d0, region_len-1)
    await dev_pf0_bar0.write_dword(0x0010d4, 0)
    # RAM stride
    await dev_pf0_bar0.write_dword(0x0010d8, block_stride)
    await dev_pf0_bar0.write_dword(0x0010dc, 0)
    # clear cycle count
    await dev_pf0_bar0.write_dword(0x001008, 0)
    await dev_pf0_bar0.write_dword(0x00100c, 0)
    # block length
    await dev_pf0_bar0.write_dword(0x001010, block_size)
    # block count
    await dev_pf0_bar0.write_dword(0x001018, block_count)
    await dev_pf0_bar0.write_dword(0x00101c, 0)
    # start
    await dev_pf0_bar0.write_dword(0x001000, 1)

    for k in range(10):
        cnt = await dev_pf0_bar0.read_dword(0x001018)
        await Timer(1000, 'ns')
        if cnt == 0:
            break

    # configure operation (write)
    # DMA base address
    await dev_pf0_bar0.write_dword(0x001180, (mem_base+dest_offset) & 0xffffffff)
    await dev_pf0_bar0.write_dword(0x001184, (mem_base+dest_offset >> 32) & 0xffffffff)
    # DMA offset address
    await dev_pf0_bar0.write_dword(0x001188, 0)
    await dev_pf0_bar0.write_dword(0x00118c, 0)
    # DMA offset mask
    await dev_pf0_bar0.write_dword(0x001190, region_len-1)
    await dev_pf0_bar0.write_dword(0x001194, 0)
    # DMA stride
    await dev_pf0_bar0.write_dword(0x001198, block_stride)
    await dev_pf0_bar0.write_dword(0x00119c, 0)
    # RAM base address
    await dev_pf0_bar0.write_dword(0x0011c0, 0)
    await dev_pf0_bar0.write_dword(0x0011c4, 0)
    # RAM offset address
    await dev_pf0_bar0.write_dword(0x0011c8, 0)
    await dev_pf0_bar0.write_dword(0x0011cc, 0)
    # RAM offset mask
    await dev_pf0_bar0.write_dword(0x0011d0, region_len-1)
    await dev_pf0_bar0.write_dword(0x0011d4, 0)
    # RAM stride
    await dev_pf0_bar0.write_dword(0x0011d8, block_stride)
    await dev_pf0_bar0.write_dword(0x0011dc, 0)
    # clear cycle count
    await dev_pf0_bar0.write_dword(0x001108, 0)
    await dev_pf0_bar0.write_dword(0x00110c, 0)
    # block length
    await dev_pf0_bar0.write_dword(0x001110, block_size)
    # block count
    await dev_pf0_bar0.write_dword(0x001118, block_count)
    await dev_pf0_bar0.write_dword(0x00111c, 0)
    # start
    await dev_pf0_bar0.write_dword(0x001100, 1)

    for k in range(10):
        cnt = await dev_pf0_bar0.read_dword(0x001118)
        await Timer(1000, 'ns')
        if cnt == 0:
            break

    tb.log.info("%s", mem.hexdump_str(dest_offset, region_len))

    assert mem[src_offset:src_offset+region_len] == mem[dest_offset:dest_offset+region_len]

    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)


# cocotb-test

tests_dir = os.path.dirname(__file__)
rtl_dir = os.path.abspath(os.path.join(tests_dir, '..', '..', 'rtl'))
lib_dir = os.path.abspath(os.path.join(rtl_dir, '..', 'lib'))
pcie_rtl_dir = os.path.abspath(os.path.join(lib_dir, 'pcie', 'rtl'))


def test_fpga_core(request):
    dut = "fpga_core"
    module = os.path.splitext(os.path.basename(__file__))[0]
    toplevel = dut

    verilog_sources = [
        os.path.join(rtl_dir, f"{dut}.v"),
        os.path.join(rtl_dir, "common", "example_core_pcie_us.v"),
        os.path.join(rtl_dir, "common", "example_core_pcie.v"),
        os.path.join(rtl_dir, "common", "example_core.v"),
        os.path.join(rtl_dir, "common", "axi_ram.v"),
        os.path.join(pcie_rtl_dir, "pcie_us_if.v"),
        os.path.join(pcie_rtl_dir, "pcie_us_if_rc.v"),
        os.path.join(pcie_rtl_dir, "pcie_us_if_rq.v"),
        os.path.join(pcie_rtl_dir, "pcie_us_if_cq.v"),
        os.path.join(pcie_rtl_dir, "pcie_us_if_cc.v"),
        os.path.join(pcie_rtl_dir, "pcie_us_cfg.v"),
        os.path.join(pcie_rtl_dir, "pcie_axil_master.v"),
        os.path.join(pcie_rtl_dir, "pcie_axi_master.v"),
        os.path.join(pcie_rtl_dir, "pcie_axi_master_rd.v"),
        os.path.join(pcie_rtl_dir, "pcie_axi_master_wr.v"),
        os.path.join(pcie_rtl_dir, "pcie_tlp_demux_bar.v"),
        os.path.join(pcie_rtl_dir, "pcie_tlp_demux.v"),
        os.path.join(pcie_rtl_dir, "pcie_tlp_mux.v"),
        os.path.join(pcie_rtl_dir, "pcie_tlp_fifo.v"),
        os.path.join(pcie_rtl_dir, "pcie_tlp_fifo_raw.v"),
        os.path.join(pcie_rtl_dir, "pcie_msix.v"),
        os.path.join(pcie_rtl_dir, "dma_if_pcie.v"),
        os.path.join(pcie_rtl_dir, "dma_if_pcie_rd.v"),
        os.path.join(pcie_rtl_dir, "dma_if_pcie_wr.v"),
        os.path.join(pcie_rtl_dir, "dma_psdpram.v"),
        os.path.join(pcie_rtl_dir, "priority_encoder.v"),
        os.path.join(pcie_rtl_dir, "pulse_merge.v"),
    ]

    parameters = {}

    parameters['AXIS_PCIE_DATA_WIDTH'] = 256
    parameters['AXIS_PCIE_KEEP_WIDTH'] = parameters['AXIS_PCIE_DATA_WIDTH'] // 32
    parameters['AXIS_PCIE_RQ_USER_WIDTH'] = 60
    parameters['AXIS_PCIE_RC_USER_WIDTH'] = 75
    parameters['AXIS_PCIE_CQ_USER_WIDTH'] = 85
    parameters['AXIS_PCIE_CC_USER_WIDTH'] = 33
    parameters['RC_STRADDLE'] = int(parameters['AXIS_PCIE_DATA_WIDTH'] >= 256)
    parameters['RQ_STRADDLE'] = int(parameters['AXIS_PCIE_DATA_WIDTH'] >= 512)
    parameters['CQ_STRADDLE'] = int(parameters['AXIS_PCIE_DATA_WIDTH'] >= 512)
    parameters['CC_STRADDLE'] = int(parameters['AXIS_PCIE_DATA_WIDTH'] >= 512)
    parameters['RQ_SEQ_NUM_WIDTH'] = 4
    parameters['RQ_SEQ_NUM_ENABLE'] = 1
    parameters['PCIE_TAG_COUNT'] = 64
    parameters['BAR0_APERTURE'] = 24
    parameters['BAR2_APERTURE'] = 24
    parameters['BAR4_APERTURE'] = 16

    extra_env = {f'PARAM_{k}': str(v) for k, v in parameters.items()}

    sim_build = os.path.join(tests_dir, "sim_build",
        request.node.name.replace('[', '-').replace(']', ''))

    cocotb_test.simulator.run(
        python_search=[tests_dir],
        verilog_sources=verilog_sources,
        toplevel=toplevel,
        module=module,
        parameters=parameters,
        sim_build=sim_build,
        extra_env=extra_env,
    )
