from django.db import models
from django.db.models.fields.related import ForeignKey

# Edge module.
class Edge(models.Model):
    name = models.CharField(verbose_name="name", help_text="Display name of edge.", max_length=32, blank=True)
    ip = models.CharField(verbose_name="IP", help_text="The edge server IP.", max_length=32)

    bgp = models.BooleanField(verbose_name="Enable BGP (AKA Announce)", help_text="Whether to enable BGP.", default=True)

    status = models.BooleanField(verbose_name="Status", editable=False, default=False)

    def __str__(self):
        return self.ip

class Edge_Stats(models.Model):
    edge_id = models.ForeignKey(Edge, on_delete=models.DO_NOTHING)
    sdate = models.DateTimeField(auto_now=True)

    bla_pckts = models.BigIntegerField(null=True, editable=False)
    bla_pckts_ps = models.BigIntegerField(null=True, editable=False)

    bla_bytes = models.BigIntegerField(null=True, editable=False)
    bla_bytes_ps = models.BigIntegerField(null=True, editable=False)

    whi_pckts = models.BigIntegerField(null=True, editable=False)
    whi_pckts_ps = models.BigIntegerField(null=True, editable=False)

    whi_bytes = models.BigIntegerField(null=True, editable=False)
    whi_bytes_ps = models.BigIntegerField(null=True, editable=False)

    blo_pckts = models.BigIntegerField(null=True, editable=False)
    blo_pckts_ps = models.BigIntegerField(null=True, editable=False)

    blo_bytes = models.BigIntegerField(null=True, editable=False)
    blo_bytes_ps = models.BigIntegerField(null=True, editable=False)

    fwd_pckts = models.BigIntegerField(null=True, editable=False)
    fwd_pckts_ps = models.BigIntegerField(null=True, editable=False)

    fwd_bytes = models.BigIntegerField(null=True, editable=False)
    fwd_bytes_ps = models.BigIntegerField(null=True, editable=False)

    fwdo_pckts = models.BigIntegerField(null=True, editable=False)
    fwdo_pckts_ps = models.BigIntegerField(null=True, editable=False)

    fwdo_bytes = models.BigIntegerField(null=True, editable=False)
    fwdo_bytes_ps = models.BigIntegerField(null=True, editable=False)

    pass_pckts = models.BigIntegerField(null=True, editable=False)
    pass_pckts_ps = models.BigIntegerField(null=True, editable=False)

    pass_bytes = models.BigIntegerField(null=True, editable=False)
    pass_bytes_ps = models.BigIntegerField(null=True, editable=False)

    bad_pckts = models.BigIntegerField(null=True, editable=False)
    bad_pckts_ps = models.BigIntegerField(null=True, editable=False)

    bad_bytes = models.BigIntegerField(null=True, editable=False)
    bad_bytes_ps = models.BigIntegerField(null=True, editable=False)

    a2rp_pckts = models.BigIntegerField(null=True, editable=False)
    a2rp_pckts_ps = models.BigIntegerField(null=True, editable=False)

    a2rp_bytes = models.BigIntegerField(null=True, editable=False)
    a2rp_bytes_ps = models.BigIntegerField(null=True, editable=False)

    a2rs_pckts = models.BigIntegerField(null=True, editable=False)
    a2rs_pckts_ps = models.BigIntegerField(null=True, editable=False)

    a2rs_bytes = models.BigIntegerField(null=True, editable=False)
    a2rs_bytes_ps = models.BigIntegerField(null=True, editable=False)

    dro_pckts = models.BigIntegerField(null=True, editable=False)
    dro_pckts_ps = models.BigIntegerField(null=True, editable=False)

    dro_bytes = models.BigIntegerField(null=True, editable=False)
    dro_bytes_ps = models.BigIntegerField(null=True, editable=False)

    drc_pckts = models.BigIntegerField(null=True, editable=False)
    drc_pckts_ps = models.BigIntegerField(null=True, editable=False)

    drc_bytes = models.BigIntegerField(null=True, editable=False)
    drc_bytes_ps = models.BigIntegerField(null=True, editable=False)

    cpu_load = models.BigIntegerField(null=True, editable=False)

class Edge_Settings(models.Model):
    class ForceMode(models.IntegerChoices):
        NONE = 0, "None (DRV)"
        SKB = 1, "SKB"
        HW = 2, "Offload"
    
    edge_id = models.ForeignKey(Edge, on_delete=models.CASCADE)
    interface = models.CharField(verbose_name="Interface", help_text="The interface for the XDP program to bind to", default="ens18", max_length=64)
    edge_ip = models.CharField(verbose_name="Edge IP", help_text="Override the interface IP (leave blank to have it retrieved automatically, recommended)", max_length=32, blank=True)
    force_mode = models.IntegerField(verbose_name="XDP Force Mode", help_text="The XDP force mode.", default=ForceMode.NONE, choices=ForceMode.choices)
    socket_count = models.IntegerField(verbose_name="Socket Count", help_text="AF_XDP socket count (0 = use CPU count).", default=0)
    queue_is_static = models.BooleanField(name="queue_is_static", verbose_name="Use Queue ID", help_text="Whether to use the below queue ID for all socket.", default=False)
    queue_id = models.IntegerField(verbose_name="Queue ID", help_text="The queue ID to use if Use Queue ID is enabled.", default=0)
    zero_copy = models.BooleanField(verbose_name="Zero Copy", help_text="Whether to enable AF_XDP zero-copy support.", default=False)
    need_wakeup = models.BooleanField(verbose_name="Need Wakeup", help_text="AF_XDP enable need wakeup (may cause better performance.", default=True)
    batch_size = models.IntegerField(verbose_name="Batch Size", help_text="AF_XDP batch size for RX.", default=64)
    verbose = models.BooleanField(verbose_name="Verbose", help_text="Whether to enable verbose mode on the edge server.", default=False)
    calc_stats = models.BooleanField(verbose_name="Calculate Stats", help_text="Whether to calculate stats to /etc/kilimanjaro.", default=True)
    allow_all_edge = models.BooleanField(verbose_name="Allow All Edge Traffic", help_text="Whether to enable all traffic sent directly to the edge depending on the edge IP.", default=True)

    class Meta:
        verbose_name = "edge setting"

    def __str__(self):
        return self.edge_id.ip +  " Settings"

# Connection module.
class Connection(models.Model):
    class Filters(models.IntegerChoices):
        NONE = 0, "None"
        SRCDS = (1 << 0), "SRCDS"
        RUST = (1 << 1), "Rust"

    enabled = models.BooleanField(verbose_name="Enabled", help_text="Enable connection.", default=True)
    
    bind_ip = models.CharField(verbose_name="Bind IP", help_text="Usually game server IP/Anycast IP", max_length=32)
    bind_port = models.IntegerField(verbose_name="Bind Port", help_text="Usually the game server port (e.g. 27015).")

    dest_ip = models.CharField(verbose_name="Dest IP", help_text="The game server machine IP.", max_length=32)
    dest_port = models.IntegerField(verbose_name="Dest Port", help_text="Port to translate to (0 = bind port, default).", default=0)

    filters = models.IntegerField(verbose_name="Filters", help_text="Filters to apply for this connection.", default=Filters.NONE, choices=Filters.choices)

    udp_rl_bl = models.IntegerField(verbose_name="UDP RL BL", help_text="UDP rate limit block time.", default=0)
    udp_rl_pps = models.IntegerField(verbose_name="UDP RL PPS", help_text="UDP rate limit PPS limit.", default=0)
    udp_rl_bps = models.IntegerField(verbose_name="UDP RL BPS", help_text="UDP rate limit BPS limit.", default=0)

    tcp_rl_bl = models.IntegerField(verbose_name="TCP RL BL", help_text="TCP rate limit block time.", default=0)
    tcp_rl_pps = models.IntegerField(verbose_name="TCP RL PPS", help_text="TCP rate limit PPS limit.", default=0)
    tcp_rl_bps = models.IntegerField(verbose_name="TCP RL BPS", help_text="TCP rate limit BPS limit.", default=0)

    icmp_rl_bl = models.IntegerField(verbose_name="ICMP RL BL", help_text="ICMP rate limit block time.", default=0)
    icmp_rl_pps = models.IntegerField(verbose_name="ICMP RL PPS", help_text="ICMP rate limit PPS limit.", default=0)
    icmp_rl_bps = models.IntegerField(verbose_name="ICMP RL BPS", help_text="ICMP rate limit BPS limit.", default=0)

    syn_rl_bl = models.IntegerField(verbose_name="SYN RL BL", help_text="TCP SYN rate limit block time.", default=0)
    syn_rl_pps = models.IntegerField(verbose_name="SYN RL PPS", help_text="TCP SYN rate limit PPS limit.", default=0)
    syn_rl_bps = models.IntegerField(verbose_name="SYN RL BPS", help_text="TCP SYN rate limit BPS limit.", default=0)

    a2s_info_enabled = models.BooleanField(verbose_name="A2S_INFO Caching", help_text="Whether to enable A2S_INFO caching.", default=False)
    a2s_info_cache_time = models.IntegerField(verbose_name="A2S_INFO Cache Time", help_text="A2S_INFO cache time if enabled.", default=45)
    a2s_info_global_cache = models.BooleanField(verbose_name="A2S_INFO Global Cache", help_text="Whether to enable A2S_INFO global caching.", default=False)

    pps = models.BigIntegerField(null=True, editable=False)
    bps = models.BigIntegerField(null=True, editable=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        ret = []
        conn = {}
        conn["enabled"] = self.enabled
        conn["bind_ip"] = self.bind_ip
        conn["bind_port"] = self.bind_port
        conn["dest_ip"] = self.dest_ip
        conn["dest_port"] = self.dest_port
        conn["filters"] = self.filters

        conn["udp_rl"] = {}
        conn["udp_rl"]["block_time"] = self.udp_rl_bl
        conn["udp_rl"]["pps"] = self.udp_rl_pps
        conn["udp_rl"]["bps"] = self.udp_rl_bps

        conn["tcp_rl"] = {}
        conn["tcp_rl"]["block_time"] = self.tcp_rl_bl
        conn["tcp_rl"]["pps"] = self.tcp_rl_pps
        conn["tcp_rl"]["bps"] = self.tcp_rl_bps

        conn["icmp_rl"] = {}
        conn["icmp_rl"]["block_time"] = self.icmp_rl_bl
        conn["icmp_rl"]["pps"] = self.icmp_rl_pps
        conn["icmp_rl"]["bps"] = self.icmp_rl_bps
        
        conn["syn_settings"] = {}
        conn["syn_settings"]["rl"] = {}
        conn["syn_settings"]["rl"]["block_time"] = self.syn_rl_bl
        conn["syn_settings"]["rl"]["pps"] = self.syn_rl_pps
        conn["syn_settings"]["rl"]["bps"] = self.syn_rl_bps

        conn["cache_settings"] = {}
        conn["cache_settings"]["a2s_info_enabled"] = self.a2s_info_enabled
        conn["cache_settings"]["a2s_info_cache_time"] = self.a2s_info_cache_time
        conn["cache_settings"]["a2s_info_global_cache"] = self.a2s_info_global_cache
        ret.append(conn)

        import asyncio
        import web_socket
        asyncio.run(web_socket.prepare_and_send_data("conn_update", connections=ret))

    def __str__(self):
        return self.bind_ip + ":" + str(self.bind_port)

class Connection_A2S_Response(models.Model):
    connection_id = ForeignKey(Connection, on_delete=models.DO_NOTHING)
    response = models.CharField(verbose_name="A2S_INFO Response", help_text="A2S_INFO response text.", max_length=2048)
    expires = models.BigIntegerField(verbose_name="Cache Expire Time", help_text="Response's expire time in nanoseconds.", null=True)

    def __str__(self):
        return self.ip + ":" + str(self.port)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        a2s = {}

        a2s["ip"] = self.connection_id.bind_ip
        a2s["port"] = self.connection_id.bind_port
        a2s["expires"] = self.expires
        a2s["response"] = self.self.response

        import asyncio
        import web_socket
        asyncio.run(web_socket.prepare_and_send_data("a2s_update", a2s_resp=a2s))

    class Meta:
        verbose_name = "A2S_INFO response"
        verbose_name_plural = "A2S_INFO responses"

class Connection_Stats(models.Model):
    connection_id = ForeignKey(Connection, on_delete=models.DO_NOTHING)
    pps = models.BigIntegerField(null=True, editable=False)
    bps = models.BigIntegerField(null=True, editable=False)

class Whitelist(models.Model):
    auto_added = models.BooleanField(verbose_name="Auto Added", help_text="Whether this was added by system", editable=False, default=False)
    prefix = models.CharField(verbose_name="Prefix", help_text="The prefix in IP/CIDR format", max_length=32)

    class Meta:
        verbose_name_plural = "whitelist IPs"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        ret = []

        ret.append(self.prefix)

        import asyncio
        import web_socket
        asyncio.run(web_socket.prepare_and_send_data("whitelist_update", whitelist=ret))

    def __str__(self):
        return self.prefix

class Blacklist(models.Model):
    auto_added = models.BooleanField(verbose_name="Auto Added", help_text="Whether this was added by system", editable=False, default=False)
    prefix = models.CharField(verbose_name="Prefix", help_text="The prefix in IP/CIDR format", max_length=32)

    class Meta:
        verbose_name_plural = "blacklist IPs"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        ret = []

        ret.append(self.prefix)

        print("From save " + str(ret))

        import asyncio
        import web_socket
        asyncio.run(web_socket.prepare_and_send_data("blacklist_update", blacklist=ret))

    def __str__(self):
        return self.prefix

class Port_Punch(models.Model):
    auto_added = models.BooleanField(verbose_name="Auto Added", help_text="Whether this was added by system", editable=False, default=False)
    ip = models.CharField(verbose_name="IP Address", help_text="IP address", max_length=32)
    port = models.IntegerField(verbose_name="Port", help_text="Port", default=0)

    service_ip = models.CharField(verbose_name="Service IP Address", help_text="Service IP address", max_length=32)
    service_port = models.IntegerField(verbose_name="Service Port", help_text="Service Port", default=0)

    dest_ip = models.CharField(verbose_name="Destination IP Address", help_text="The game server machine's IP address", max_length=32)

    def __str__(self):
        return self.ip + ":" + str(self.port)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        ret = []
        pp = {}

        pp["ip"] = self.ip
        pp["port"] = self.port
        pp["service_ip"] = self.service_ip
        pp["service_port"] = self.service_port

        pp["dest_ip"] = self.dest_ip

        ret.append(pp)

        import asyncio
        import web_socket
        asyncio.run(web_socket.prepare_and_send_data("port_punch_update", port_punch=ret))

    class Meta:
        verbose_name = "port punch"
        verbose_name_plural = "port punches"