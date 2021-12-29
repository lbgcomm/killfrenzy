# Generated by Django 4.0 on 2021-12-29 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blacklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_added', models.BooleanField(default=False, editable=False, help_text='Whether this was added by system', verbose_name='Auto Added')),
                ('prefix', models.CharField(help_text='The prefix in IP/CIDR format', max_length=32, verbose_name='Prefix')),
            ],
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=True, help_text='Enable connection', verbose_name='Enabled')),
                ('bind_ip', models.CharField(help_text='Usually game server IP/Anycast IP', max_length=32, verbose_name='Bind IP')),
                ('bind_port', models.IntegerField(help_text='Usually the game server port (e.g. 27015)', verbose_name='Bind Port')),
                ('dest_ip', models.CharField(help_text='The game server machine IP', max_length=32, verbose_name='Dest IP')),
                ('dest_port', models.IntegerField(default=0, help_text='Port to translate to (0 = bind port, default)', verbose_name='Dest Port')),
                ('filters', models.IntegerField(choices=[(0, 'None'), (1, 'SRCDS'), (2, 'Rust')], default=0, help_text='Filters to apply for this connection', verbose_name='Filters')),
                ('udp_rl_bl', models.IntegerField(default=0, help_text='UDP rate limit block time', verbose_name='UDP RL BL')),
                ('udp_rl_pps', models.IntegerField(default=0, help_text='UDP rate limit PPS limit', verbose_name='UDP RL PPS')),
                ('udp_rl_bps', models.IntegerField(default=0, help_text='UDP rate limit BPS limit', verbose_name='UDP RL BPS')),
                ('tcp_rl_bl', models.IntegerField(default=0, help_text='TCP rate limit block time', verbose_name='TCP RL BL')),
                ('tcp_rl_pps', models.IntegerField(default=0, help_text='TCP rate limit PPS limit', verbose_name='TCP RL PPS')),
                ('tcp_rl_bps', models.IntegerField(default=0, help_text='TCP rate limit BPS limit', verbose_name='TCP RL BPS')),
                ('icmp_rl_bl', models.IntegerField(default=0, help_text='ICMP rate limit block time', verbose_name='ICMP RL BL')),
                ('icmp_rl_pps', models.IntegerField(default=0, help_text='ICMP rate limit PPS limit', verbose_name='ICMP RL PPS')),
                ('icmp_rl_bps', models.IntegerField(default=0, help_text='ICMP rate limit BPS limit', verbose_name='ICMP RL BPS')),
                ('syn_rl_bl', models.IntegerField(default=0, help_text='TCP SYN rate limit block time', verbose_name='SYN RL BL')),
                ('syn_rl_pps', models.IntegerField(default=0, help_text='TCP SYN rate limit PPS limit', verbose_name='SYN RL PPS')),
                ('syn_rl_bps', models.IntegerField(default=0, help_text='TCP SYN rate limit BPS limit', verbose_name='SYN RL BPS')),
                ('a2s_info_enabled', models.BooleanField(default=False, help_text='Whether to enable A2S_INFO caching', verbose_name='A2S_INFO Caching')),
                ('a2s_info_cache_time', models.IntegerField(default=45, help_text='A2S_INFO cache time if enabled', verbose_name='A2S_INFO Cache Time')),
            ],
        ),
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(help_text='The edge server IP.', max_length=32, verbose_name='IP')),
                ('bgp', models.BooleanField(default=True, help_text='Whether to enable BGP.', verbose_name='Enable BGP (AKA Announce)')),
                ('bla_pckts', models.BigIntegerField(editable=False)),
                ('bla_pckts_ps', models.BigIntegerField(editable=False)),
                ('bla_bytes', models.BigIntegerField(editable=False)),
                ('bla_bytes_ps', models.BigIntegerField(editable=False)),
                ('whi_pckts', models.BigIntegerField(editable=False)),
                ('whi_pckts_ps', models.BigIntegerField(editable=False)),
                ('whi_bytes', models.BigIntegerField(editable=False)),
                ('whi_bytes_ps', models.BigIntegerField(editable=False)),
                ('blo_pckts', models.BigIntegerField(editable=False)),
                ('blo_pckts_ps', models.BigIntegerField(editable=False)),
                ('blo_bytes', models.BigIntegerField(editable=False)),
                ('blo_bytes_ps', models.BigIntegerField(editable=False)),
                ('fwd_pckts', models.BigIntegerField(editable=False)),
                ('fwd_pckts_ps', models.BigIntegerField(editable=False)),
                ('fwd_bytes', models.BigIntegerField(editable=False)),
                ('fwd_bytes_ps', models.BigIntegerField(editable=False)),
                ('pass_pckts', models.BigIntegerField(editable=False)),
                ('pass_pckts_ps', models.BigIntegerField(editable=False)),
                ('pass_bytes', models.BigIntegerField(editable=False)),
                ('pass_bytes_ps', models.BigIntegerField(editable=False)),
                ('bad_pckts', models.BigIntegerField(editable=False)),
                ('bad_pckts_ps', models.BigIntegerField(editable=False)),
                ('bad_bytes', models.BigIntegerField(editable=False)),
                ('bad_bytes_ps', models.BigIntegerField(editable=False)),
                ('a2rp_pckts', models.BigIntegerField(editable=False)),
                ('a2rp_pckts_ps', models.BigIntegerField(editable=False)),
                ('a2rp_bytes', models.BigIntegerField(editable=False)),
                ('a2rp_bytes_ps', models.BigIntegerField(editable=False)),
                ('a2rs_pckts', models.BigIntegerField(editable=False)),
                ('a2rs_pckts_ps', models.BigIntegerField(editable=False)),
                ('a2rs_bytes', models.BigIntegerField(editable=False)),
                ('a2rs_bytes_ps', models.BigIntegerField(editable=False)),
                ('dro_pckts', models.BigIntegerField(editable=False)),
                ('dro_pckts_ps', models.BigIntegerField(editable=False)),
                ('dro_bytes', models.BigIntegerField(editable=False)),
                ('dro_bytes_ps', models.BigIntegerField(editable=False)),
                ('drc_pckts', models.BigIntegerField(editable=False)),
                ('drc_pckts_ps', models.BigIntegerField(editable=False)),
                ('drc_bytes', models.BigIntegerField(editable=False)),
                ('drc_bytes_ps', models.BigIntegerField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Port_Punch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_added', models.BooleanField(default=False, editable=False, help_text='Whether this was added by system', verbose_name='Auto Added')),
                ('ip', models.CharField(help_text='IP address', max_length=32, verbose_name='IP Address')),
                ('port', models.IntegerField(default=0, help_text='Port', verbose_name='Port')),
            ],
            options={
                'verbose_name': 'port punch',
                'verbose_name_plural': 'port punches',
            },
        ),
        migrations.CreateModel(
            name='Whitelist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_added', models.BooleanField(default=False, editable=False, help_text='Whether this was added by system', verbose_name='Auto Added')),
                ('prefix', models.CharField(help_text='The prefix in IP/CIDR format', max_length=32, verbose_name='Prefix')),
            ],
        ),
        migrations.CreateModel(
            name='Edge_Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interface', models.CharField(default='ens18', help_text='The interface for the XDP program to bind to', max_length=64, verbose_name='Interface')),
                ('edge_ip', models.CharField(blank=True, help_text='Override the interface IP (leave blank to have it retrieved automatically, recommended)', max_length=32, verbose_name='Edge IP')),
                ('force_mode', models.IntegerField(choices=[(0, 'None (DRV)'), (1, 'SKB'), (2, 'Offload')], default=0, help_text='The XDP force mode.', verbose_name='XDP Force Mode')),
                ('socket_count', models.IntegerField(default=0, help_text='AF_XDP socket count (0 = use CPU count).', verbose_name='Socket Count')),
                ('queue_is_static', models.BooleanField(default=False, help_text='Whether to use the below queue ID for all socket.', verbose_name='Use Queue ID')),
                ('queue_id', models.IntegerField(default=0, help_text='The queue ID to use if Use Queue ID is enabled.', verbose_name='Queue ID')),
                ('zero_copy', models.BooleanField(default=False, help_text='Whether to enable AF_XDP zero-copy support.', verbose_name='Zero Copy')),
                ('need_wakeup', models.BooleanField(default=True, help_text='AF_XDP enable need wakeup (may cause better performance.', verbose_name='Need Wakeup')),
                ('batch_size', models.IntegerField(default=64, help_text='AF_XDP batch size for RX.', verbose_name='Batch Size')),
                ('verbose', models.BooleanField(default=False, help_text='Whether to enable verbose mode on the edge server.', verbose_name='Verbose')),
                ('calc_stats', models.BooleanField(default=True, help_text='Whether to calculate stats to /etc/kilimanjaro.', verbose_name='Calculate Stats')),
                ('allow_all_edge', models.BooleanField(default=True, help_text='Whether to enable all traffic sent directly to the edge depending on the edge IP.', verbose_name='Allow All Edge Traffic')),
                ('edge_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='connections.edge')),
            ],
            options={
                'verbose_name': 'edge setting',
            },
        ),
    ]
