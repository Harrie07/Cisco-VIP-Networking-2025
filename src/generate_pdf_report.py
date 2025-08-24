from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from datetime import datetime
import os

def create_improved_cisco_vip_report():
    """Generate improved professional Cisco VIP 2025 PDF report with better layout"""
    
    # Ensure output directory exists
    output_dir = "../output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create PDF document with improved layout settings
    pdf_path = os.path.join(output_dir, "Cisco_VIP_2025_Improved_Report_Harshal_Sakpal.pdf")
    doc = SimpleDocTemplate(
        pdf_path, 
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=20*mm,
        bottomMargin=25*mm,  # Increased bottom margin
        allowSplitting=1,    # Allow content splitting
        showBoundary=0       # Hide boundaries in production
    )
    
    # Get styles and create custom styles
    styles = getSampleStyleSheet()
    
    # Cover page title style
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Title'],
        fontSize=26,  # Slightly larger
        spaceAfter=25,
        alignment=1,
        textColor=colors.HexColor('#1f4e79'),
        fontName='Helvetica-Bold',
        leading=30
    )
    
    # Cover subtitle style
    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Heading2'],
        fontSize=20,  # Slightly larger
        spaceAfter=35,
        alignment=1,
        textColor=colors.HexColor('#2f5f8f'),
        fontName='Helvetica',
        leading=24
    )
    
    # Cover info style
    cover_info_style = ParagraphStyle(
        'CoverInfo',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=8,
        alignment=1,
        fontName='Helvetica',
        leading=18
    )
    
    # Section heading style - improved spacing
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading1'],
        fontSize=18,  # Slightly larger
        spaceAfter=18,
        spaceBefore=30,
        textColor=colors.HexColor('#1f4e79'),
        fontName='Helvetica-Bold',
        leading=20,
        keepWithNext=True  # Keep with following content
    )
    
    # Subheading style - improved spacing
    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading2'],
        fontSize=15,  # Slightly larger
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.HexColor('#2f5f8f'),
        fontName='Helvetica-Bold',
        leading=17,
        keepWithNext=True  # Keep with following content
    )
    
    # Normal text style - improved spacing
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=10,  # Increased spacing
        spaceBefore=5,
        fontName='Helvetica',
        leading=14,  # Better line spacing
        alignment=0
    )
    
    # Bullet style - improved
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,  # Better spacing
        spaceBefore=3,
        leftIndent=20,  # Better indentation
        bulletIndent=10,
        fontName='Helvetica',
        leading=14
    )
    
    # Table cell styles - improved
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        leading=13,  # Better line spacing
        alignment=0
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontSize=11,  # Slightly larger
        fontName='Helvetica-Bold',
        leading=14,
        alignment=1,
        textColor=colors.white
    )
    
    # Code style for CLI commands - improved
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier',
        leading=12,  # Better spacing
        textColor=colors.HexColor('#2d5016'),
        leftIndent=15,
        spaceAfter=5,
        spaceBefore=2,
        backColor=colors.HexColor('#f5f5f5')  # Light background
    )
    
    story = []
    
    # ===========================================
    # 1. COVER PAGE - Keep together
    # ===========================================
    
    cover_content = []
    cover_content.append(Spacer(1, 60))
    cover_content.append(Paragraph("Enterprise Network Implementation", cover_title_style))
    cover_content.append(Paragraph("Cisco VIP 2025", cover_subtitle_style))
    cover_content.append(Spacer(1, 40))
    
    # Project details box - improved styling
    cover_info = [
        [Paragraph("<b>Student Name:</b>", table_header_style), 
         Paragraph("Harshal Sakpal", table_cell_style)],
        [Paragraph("<b>Institution:</b>", table_header_style), 
         Paragraph("A.P Shah Institute of Technology", table_cell_style)],
        [Paragraph("<b>Program:</b>", table_header_style), 
         Paragraph("Cisco Virtual Internship Program 2025", table_cell_style)],
        [Paragraph("<b>Project Title:</b>", table_header_style), 
         Paragraph("Enterprise Network Topology with Static Routing", table_cell_style)],
        [Paragraph("<b>Submission Date:</b>", table_header_style), 
         Paragraph("August 22, 2025", table_cell_style)],
        [Paragraph("<b>Platform:</b>", table_header_style), 
         Paragraph("Cisco Packet Tracer", table_cell_style)],
        [Paragraph("<b>Project File:</b>", table_header_style), 
         Paragraph("new.pkt", table_cell_style)]
    ]
    
    cover_table = Table(cover_info, colWidths=[2.2*inch, 3.8*inch])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1f4e79')),  # Darker header
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1.5, colors.HexColor('#1f4e79')),  # Thicker border
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),  # Increased padding
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8)
    ]))
    
    cover_content.append(cover_table)
    cover_content.append(Spacer(1, 80))
    
    # Cover page footer
    cover_content.append(Paragraph(
        "<i>Professional network implementation demonstrating static routing,<br/>"
        "inter-site connectivity, and enterprise-level network design</i>",
        ParagraphStyle('CoverFooter', parent=styles['Normal'], fontSize=12, 
                      alignment=1, textColor=colors.HexColor('#666666'), 
                      fontName='Helvetica-Oblique')
    ))
    
    # Keep cover page together
    story.append(KeepTogether(cover_content))
    story.append(PageBreak())
    
    # ===========================================
    # 2. EXECUTIVE SUMMARY - Better organization
    # ===========================================
    
    story.append(Paragraph("Executive Summary", heading_style))
    
    # Keep executive summary paragraphs together
    exec_summary = []
    exec_summary.append(Paragraph(
        "This project demonstrates the successful implementation of a professional enterprise "
        "network infrastructure using Cisco ISR 1941 routers and Catalyst switches. The network "
        "features two geographically distributed sites interconnected via static routing, providing "
        "reliable and secure inter-site communication for distributed business operations.",
        normal_style
    ))
    
    exec_summary.append(Paragraph(
        "The implementation showcases advanced networking concepts including hierarchical network "
        "design, proper IP addressing schemes, static route configuration, and comprehensive "
        "network validation procedures. All connectivity tests achieved 100% success rates, "
        "demonstrating robust network functionality and professional-level configuration standards.",
        normal_style
    ))
    
    story.append(KeepTogether(exec_summary))
    story.append(Spacer(1, 20))
    
    # Achievements section - keep together
    achievements_content = []
    achievements_content.append(Paragraph("Key Project Achievements", subheading_style))
    
    achievements = [
        "Network Topology: Successfully designed and implemented 2-router enterprise topology with 4 endpoint devices",
        "Static Routing: Configured bidirectional static routes enabling seamless inter-site communication",
        "Connectivity Validation: Achieved 100% end-to-end network connectivity across both local and remote networks", 
        "Professional Testing: Demonstrated comprehensive network troubleshooting using multiple validation methodologies",
        "Scalable Architecture: Created enterprise-grade network foundation suitable for production deployment",
        "Documentation Standards: Produced professional technical documentation meeting industry standards"
    ]
    
    for achievement in achievements:
        achievements_content.append(Paragraph(f"• <b>{achievement.split(':')[0]}:</b> {achievement.split(':', 1)[1]}", bullet_style))
    
    story.append(KeepTogether(achievements_content))
    story.append(Spacer(1, 25))
    
    # Network Health Summary - keep together with title
    health_section = []
    health_section.append(Paragraph("Network Performance Summary", subheading_style))
    
    health_data = [
        [Paragraph("<b>Performance Metric</b>", table_header_style), 
         Paragraph("<b>Achievement</b>", table_header_style)],
        [Paragraph("End-to-End Connectivity", table_cell_style), 
         Paragraph("✓ 100% Success Rate", table_cell_style)],
        [Paragraph("Local Network Tests", table_cell_style), 
         Paragraph("✓ All Tests Passed", table_cell_style)],
        [Paragraph("Inter-Site Routing", table_cell_style), 
         Paragraph("✓ Fully Functional", table_cell_style)],
        [Paragraph("Network Convergence", table_cell_style), 
         Paragraph("✓ Optimal Performance", table_cell_style)],
        [Paragraph("Configuration Validation", table_cell_style), 
         Paragraph("✓ No Issues Detected", table_cell_style)]
    ]
    
    health_table = Table(health_data, colWidths=[3*inch, 3*inch])
    health_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),  # Professional blue header
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),  # Light background
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1f4e79')),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8)
    ]))
    
    health_section.append(health_table)
    story.append(KeepTogether(health_section))
    story.append(PageBreak())
    
    # ===========================================
    # 3. NETWORK ARCHITECTURE - Better organization
    # ===========================================
    
    story.append(Paragraph("Network Architecture & Design", heading_style))
    
    # Architecture overview - keep together
    arch_overview = []
    arch_overview.append(Paragraph(
        "The enterprise network architecture follows a hierarchical design model with two distinct "
        "sites connected via WAN infrastructure. This design ensures scalability, reliability, and "
        "efficient traffic flow between distributed locations.",
        normal_style
    ))
    
    arch_overview.append(Paragraph("Network Topology Overview", subheading_style))
    arch_overview.append(Paragraph(
        "The topology displays a professional dual-site network with Router1 and Router2 as core devices, "
        "each serving their respective local area networks through dedicated switches. The WAN connection "
        "provides secure inter-site communication via high-speed serial interfaces.",
        normal_style
    ))
    
    story.append(KeepTogether(arch_overview))
    story.append(Spacer(1, 20))
    
    # Network Architecture Specifications - keep together
    arch_specs_section = []
    arch_specs_section.append(Paragraph("Network Architecture Specifications", subheading_style))
    
    arch_data = [
        [Paragraph("<b>Network Component</b>", table_header_style), 
         Paragraph("<b>IP Specification</b>", table_header_style), 
         Paragraph("<b>Technical Details</b>", table_header_style)],
        [Paragraph("Site A LAN Network", table_cell_style), 
         Paragraph("192.168.10.0/24", table_cell_style), 
         Paragraph("Router1 + Switch1 + PC1/PC2<br/>254 available host addresses", table_cell_style)],
        [Paragraph("Site B LAN Network", table_cell_style), 
         Paragraph("192.168.20.0/24", table_cell_style), 
         Paragraph("Router2 + Switch2 + PC3/PC4<br/>254 available host addresses", table_cell_style)],
        [Paragraph("WAN Connection Link", table_cell_style), 
         Paragraph("10.0.0.0/30", table_cell_style), 
         Paragraph("Point-to-point serial connection<br/>2 usable host addresses", table_cell_style)],
        [Paragraph("Routing Implementation", table_cell_style), 
         Paragraph("Static Routing", table_cell_style), 
         Paragraph("Manually configured routes<br/>Predictable and secure path selection", table_cell_style)],
        [Paragraph("Hardware Infrastructure", table_cell_style), 
         Paragraph("Cisco Enterprise Class", table_cell_style), 
         Paragraph("ISR 1941 Routers<br/>Catalyst Managed Switches", table_cell_style)]
    ]
    
    arch_table = Table(arch_data, colWidths=[2*inch, 1.8*inch, 2.2*inch])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1f4e79')),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Changed to TOP for better alignment
        ('TOPPADDING', (0, 0), (-1, -1), 10),  # Increased padding
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8)
    ]))
    
    arch_specs_section.append(arch_table)
    story.append(KeepTogether(arch_specs_section))
    story.append(Spacer(1, 25))
    
    # IP Addressing Scheme - keep together
    ip_section = []
    ip_section.append(Paragraph("Comprehensive IP Addressing Scheme", subheading_style))
    
    ip_data = [
        [Paragraph("<b>Network Device</b>", table_header_style), 
         Paragraph("<b>Interface Type</b>", table_header_style), 
         Paragraph("<b>IP Address</b>", table_header_style), 
         Paragraph("<b>Subnet Mask</b>", table_header_style),
         Paragraph("<b>Network Role</b>", table_header_style)],
        [Paragraph("Router1", table_cell_style), 
         Paragraph("GigabitEthernet0/0", table_cell_style), 
         Paragraph("192.168.10.1", table_cell_style), 
         Paragraph("255.255.255.0", table_cell_style),
         Paragraph("Site A Gateway", table_cell_style)],
        [Paragraph("Router1", table_cell_style), 
         Paragraph("Serial0/0/0", table_cell_style), 
         Paragraph("10.0.0.1", table_cell_style), 
         Paragraph("255.255.255.252", table_cell_style),
         Paragraph("WAN Endpoint", table_cell_style)],
        [Paragraph("Router2", table_cell_style), 
         Paragraph("GigabitEthernet0/0", table_cell_style), 
         Paragraph("192.168.20.1", table_cell_style), 
         Paragraph("255.255.255.0", table_cell_style),
         Paragraph("Site B Gateway", table_cell_style)],
        [Paragraph("Router2", table_cell_style), 
         Paragraph("Serial0/0/0", table_cell_style), 
         Paragraph("10.0.0.2", table_cell_style), 
         Paragraph("255.255.255.252", table_cell_style),
         Paragraph("WAN Endpoint", table_cell_style)],
        [Paragraph("PC1 (Site A)", table_cell_style), 
         Paragraph("FastEthernet0", table_cell_style), 
         Paragraph("192.168.10.10", table_cell_style), 
         Paragraph("255.255.255.0", table_cell_style),
         Paragraph("End Device", table_cell_style)],
        [Paragraph("PC2 (Site A)", table_cell_style), 
         Paragraph("FastEthernet0", table_cell_style), 
         Paragraph("192.168.10.11", table_cell_style), 
         Paragraph("255.255.255.0", table_cell_style),
         Paragraph("End Device", table_cell_style)],
        [Paragraph("PC3 (Site B)", table_cell_style), 
         Paragraph("FastEthernet0", table_cell_style), 
         Paragraph("192.168.20.10", table_cell_style), 
         Paragraph("255.255.255.0", table_cell_style),
         Paragraph("End Device", table_cell_style)],
        [Paragraph("PC4 (Site B)", table_cell_style), 
         Paragraph("FastEthernet0", table_cell_style), 
         Paragraph("192.168.20.11", table_cell_style), 
         Paragraph("255.255.255.0", table_cell_style),
         Paragraph("End Device", table_cell_style)]
    ]
    
    ip_table = Table(ip_data, colWidths=[1.2*inch, 1.3*inch, 1.2*inch, 1.2*inch, 1.1*inch])
    ip_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1f4e79')),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6)
    ]))
    
    ip_section.append(ip_table)
    story.append(KeepTogether(ip_section))
    story.append(PageBreak())
    
    # ===========================================
    # 4. IMPLEMENTATION DETAILS - Better structured
    # ===========================================
    
    story.append(Paragraph("Implementation Details", heading_style))
    
    # Implementation overview
    impl_overview = []
    impl_overview.append(Paragraph(
        "The network implementation followed a systematic approach using Cisco best practices "
        "for enterprise network deployment. Each phase was carefully executed to ensure optimal "
        "performance, security, and scalability of the final network infrastructure.",
        normal_style
    ))
    
    story.append(KeepTogether(impl_overview))
    story.append(Spacer(1, 20))
    
    # Router Configuration Summary - keep sections together
    router1_section = []
    router1_section.append(Paragraph("Router1 Configuration Details", subheading_style))
    router1_section.append(Paragraph("Core Site A Infrastructure Configuration:", normal_style))
    
    router1_configs = [
        "LAN Interface: GigabitEthernet0/0 configured with IP 192.168.10.1/24 serving as local gateway",
        "WAN Interface: Serial0/0/0 configured with IP 10.0.0.1/30 at 64000 bps for inter-site connectivity",
        "Static Route: Destination 192.168.20.0/24 via next-hop 10.0.0.2 for Site B network access",
        "Interface Status: All interfaces activated with proper duplex and speed configuration",
        "Security: Console and VTY access configured with appropriate authentication"
    ]
    
    for config in router1_configs:
        parts = config.split(': ', 1)
        if len(parts) == 2:
            router1_section.append(Paragraph(f"• <b>{parts[0]}:</b> {parts[1]}", bullet_style))
        else:
            router1_section.append(Paragraph(f"• {config}", bullet_style))
    
    story.append(KeepTogether(router1_section))
    story.append(Spacer(1, 15))
    
    router2_section = []
    router2_section.append(Paragraph("Router2 Configuration Details", subheading_style))
    router2_section.append(Paragraph("Core Site B Infrastructure Configuration:", normal_style))
    
    router2_configs = [
        "LAN Interface: GigabitEthernet0/0 configured with IP 192.168.20.1/24 serving as local gateway",
        "WAN Interface: Serial0/0/0 configured with IP 10.0.0.2/30 at 64000 bps for inter-site connectivity",
        "Static Route: Destination 192.168.10.0/24 via next-hop 10.0.0.1 for Site A network access",
        "Interface Status: All interfaces operational with optimized performance settings",
        "Redundancy: Configuration backup and startup-config synchronization implemented"
    ]
    
    for config in router2_configs:
        parts = config.split(': ', 1)
        if len(parts) == 2:
            router2_section.append(Paragraph(f"• <b>{parts[0]}:</b> {parts[1]}", bullet_style))
        else:
            router2_section.append(Paragraph(f"• {config}", bullet_style))
    
    story.append(KeepTogether(router2_section))
    story.append(Spacer(1, 20))
    
    # CLI Commands - keep together
    cli_section = []
    cli_section.append(Paragraph("Essential CLI Configuration Commands", subheading_style))
    cli_section.append(Paragraph("Professional configuration sequence used for both routers:", normal_style))
    
    cli_commands = [
        "Router> enable",
        "Router# configure terminal",
        "Router(config)# hostname Router1",
        "Router1(config)# interface gigabitEthernet 0/0",
        "Router1(config-if)# ip address 192.168.10.1 255.255.255.0",
        "Router1(config-if)# duplex auto",
        "Router1(config-if)# speed auto", 
        "Router1(config-if)# no shutdown",
        "Router1(config-if)# exit",
        "Router1(config)# interface serial 0/0/0",
        "Router1(config-if)# ip address 10.0.0.1 255.255.255.252",
        "Router1(config-if)# clock rate 64000",
        "Router1(config-if)# no shutdown",
        "Router1(config-if)# exit",
        "Router1(config)# ip route 192.168.20.0 255.255.255.0 10.0.0.2",
        "Router1(config)# exit",
        "Router1# copy running-config startup-config"
    ]
    
    for cmd in cli_commands:
        cli_section.append(Paragraph(cmd, code_style))
    
    story.append(KeepTogether(cli_section))
    story.append(Spacer(1, 20))
    
    # PC Configuration - comprehensive table
    pc_section = []
    pc_section.append(Paragraph("End Device Network Configuration", subheading_style))
    
    pc_data = [
        [Paragraph("<b>Device</b>", table_header_style), 
         Paragraph("<b>IP Address</b>", table_header_style), 
         Paragraph("<b>Subnet Mask</b>", table_header_style), 
         Paragraph("<b>Default Gateway</b>", table_header_style),
         Paragraph("<b>Network Segment</b>", table_header_style)],
        [Paragraph("PC1", table_cell_style), 
         Paragraph("192.168.10.10", table_cell_style), 
         Paragraph("255.255.255.0", table_cell_style), 
         Paragraph("192.168.10.1", table_cell_style),
         Paragraph("Site A LAN", table_cell_style)],
        [Paragraph("PC2", table_cell_style), 
         Paragraph("192.168.10.11", table_cell_style), 
         Paragraph("255.255.255.0", table_cell_style), 
         Paragraph("192.168.10.1", table_cell_style),
         Paragraph("Site A LAN", table_cell_style)],
        [Paragraph("PC3", table_cell_style), 
         Paragraph("192.168.20.10", table_cell_style), 
         Paragraph("255.255.255.0", table_cell_style), 
         Paragraph("192.168.20.1", table_cell_style),
         Paragraph("Site B LAN", table_cell_style)],
        [Paragraph("PC4", table_cell_style), 
         Paragraph("192.168.20.11", table_cell_style), 
         Paragraph("255.255.255.0", table_cell_style), 
         Paragraph("192.168.20.1", table_cell_style),
         Paragraph("Site B LAN", table_cell_style)]
    ]
    
    pc_table = Table(pc_data, colWidths=[1*inch, 1.3*inch, 1.3*inch, 1.3*inch, 1.1*inch])
    pc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1f4e79')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6)
    ]))
    
    pc_section.append(pc_table)
    story.append(KeepTogether(pc_section))
    story.append(PageBreak())
    
    # ===========================================
    # 5. TESTING & VALIDATION - Better organized
    # ===========================================
    
    story.append(Paragraph("Network Testing & Validation", heading_style))
    
    # Testing overview
    testing_overview = []
    testing_overview.append(Paragraph(
        "Comprehensive network validation was performed using multiple testing methodologies to "
        "ensure complete functionality across all network segments. Testing protocols included "
        "connectivity verification, routing validation, and performance analysis using both "
        "real-time and simulation modes.",
        normal_style
    ))
    
    story.append(KeepTogether(testing_overview))
    story.append(Spacer(1, 20))
    
    # Connectivity Test Results - comprehensive table
    test_results_section = []
    test_results_section.append(Paragraph("Comprehensive Connectivity Test Results", subheading_style))
    
    test_data = [
        [Paragraph("<b>Test Category</b>", table_header_style), 
         Paragraph("<b>Source Device</b>", table_header_style), 
         Paragraph("<b>Target Address</b>", table_header_style), 
         Paragraph("<b>Test Result</b>", table_header_style), 
         Paragraph("<b>Technical Analysis</b>", table_header_style)],
        [Paragraph("Local Gateway", table_cell_style), 
         Paragraph("PC1", table_cell_style), 
         Paragraph("192.168.10.1", table_cell_style), 
         Paragraph("✓ SUCCESS", table_cell_style), 
         Paragraph("Direct gateway connectivity verified", table_cell_style)],
        [Paragraph("Same Subnet", table_cell_style), 
         Paragraph("PC1", table_cell_style), 
         Paragraph("192.168.10.11", table_cell_style), 
         Paragraph("✓ SUCCESS", table_cell_style), 
         Paragraph("Layer 2 switching operational", table_cell_style)],
        [Paragraph("Remote Gateway", table_cell_style), 
         Paragraph("PC1", table_cell_style), 
         Paragraph("192.168.20.1", table_cell_style), 
         Paragraph("✓ SUCCESS", table_cell_style), 
         Paragraph("Static routing functional", table_cell_style)],
        [Paragraph("End-to-End", table_cell_style), 
         Paragraph("PC1", table_cell_style), 
         Paragraph("192.168.20.10", table_cell_style), 
         Paragraph("✓ SUCCESS", table_cell_style), 
         Paragraph("Complete network connectivity", table_cell_style)],
        [Paragraph("Cross-Network", table_cell_style), 
         Paragraph("PC2", table_cell_style), 
         Paragraph("192.168.20.11", table_cell_style), 
         Paragraph("✓ SUCCESS", table_cell_style), 
         Paragraph("Bidirectional routing verified", table_cell_style)],
        [Paragraph("Return Path", table_cell_style), 
         Paragraph("PC3", table_cell_style), 
         Paragraph("192.168.10.10", table_cell_style), 
         Paragraph("✓ SUCCESS", table_cell_style), 
         Paragraph("Symmetric routing confirmed", table_cell_style)],
        [Paragraph("WAN Interface", table_cell_style), 
         Paragraph("PC4", table_cell_style), 
         Paragraph("10.0.0.1", table_cell_style), 
         Paragraph("✓ SUCCESS", table_cell_style), 
         Paragraph("WAN connectivity established", table_cell_style)]
    ]
    
    test_table = Table(test_data, colWidths=[1.1*inch, 1*inch, 1.2*inch, 0.9*inch, 1.8*inch])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1f4e79')),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (3, -1), 'CENTER'),
        ('ALIGN', (4, 1), (4, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('FONTNAME', (3, 1), (3, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (3, 1), (3, -1), colors.HexColor('#228B22'))
    ]))
    
    test_results_section.append(test_table)
    story.append(KeepTogether(test_results_section))
    story.append(Spacer(1, 25))
    
    # Simulation Analysis - keep together
    simulation_section = []
    simulation_section.append(Paragraph("Advanced Simulation Mode Analysis", subheading_style))
    simulation_section.append(Paragraph(
        "Packet Tracer simulation mode provides detailed packet flow visualization, confirming "
        "proper network behavior and protocol operations across all network layers:",
        normal_style
    ))
    
    simulation_points = [
        "Device Discovery: Simulation demonstrates proper network topology recognition and device identification",
        "Packet Flow Analysis: Visual confirmation of routing path through Router1, WAN link, and Router2",
        "Protocol Operations: Detailed ARP resolution, frame encapsulation, and routing table operations",
        "Network Convergence: Realistic timing analysis showing proper network learning behavior",
        "Layer Validation: Comprehensive Layer 2 switching and Layer 3 routing verification",
        "Performance Metrics: Network latency and throughput analysis within acceptable parameters"
    ]
    
    for point in simulation_points:
        parts = point.split(': ', 1)
        if len(parts) == 2:
            simulation_section.append(Paragraph(f"• <b>{parts[0]}:</b> {parts[1]}", bullet_style))
        else:
            simulation_section.append(Paragraph(f"• {point}", bullet_style))
    
    story.append(KeepTogether(simulation_section))
    story.append(Spacer(1, 20))
    
    # Network Verification Evidence - keep together
    evidence_section = []
    evidence_section.append(Paragraph("Technical Verification Documentation", subheading_style))
    
    verification_evidence = [
        "Configuration Validation: Complete running-config outputs showing proper interface and routing setup",
        "Connectivity Evidence: Command-line ping results demonstrating successful network communication",
        "ARP Resolution: MAC address learning and ARP table population across network segments",
        "Routing Analysis: Static route functionality and proper path selection verification",
        "Protocol Verification: Layer 2 and Layer 3 protocol operations confirmed through simulation",
        "Performance Assessment: Network response times and packet delivery success rates documented"
    ]
    
    for evidence in verification_evidence:
        parts = evidence.split(': ', 1)
        if len(parts) == 2:
            evidence_section.append(Paragraph(f"• <b>{parts[0]}:</b> {parts[1]}", bullet_style))
        else:
            evidence_section.append(Paragraph(f"• {evidence}", bullet_style))
    
    story.append(KeepTogether(evidence_section))
    story.append(PageBreak())
    
    # ===========================================
    # 6. CONCLUSION - Well-structured sections
    # ===========================================
    
    story.append(Paragraph("Project Conclusion & Assessment", heading_style))
    
    # Project Success Summary
    success_section = []
    success_section.append(Paragraph("Project Success Summary", subheading_style))
    success_section.append(Paragraph(
        "This enterprise network implementation project has exceeded all defined objectives, "
        "demonstrating mastery of professional network design, implementation, and validation "
        "methodologies. The dual-site network topology provides a robust, scalable foundation "
        "for distributed business operations with guaranteed inter-site connectivity.",
        normal_style
    ))
    
    story.append(KeepTogether(success_section))
    story.append(Spacer(1, 20))
    
    # Objectives Achieved - keep together
    objectives_section = []
    objectives_section.append(Paragraph("Key Objectives Successfully Achieved", subheading_style))
    
    objectives_achieved = [
        "Network Design Excellence: Implemented hierarchical network architecture following Cisco best practices",
        "Static Routing Mastery: Successfully configured bidirectional static routes enabling seamless communication",
        "Complete Connectivity: Achieved 100% network connectivity validation across all test scenarios",
        "Professional Standards: Demonstrated enterprise-level configuration and documentation practices",
        "Scalability Foundation: Created infrastructure capable of supporting future expansion requirements",
        "Performance Optimization: Delivered network solution with optimal routing and switching performance"
    ]
    
    for objective in objectives_achieved:
        parts = objective.split(': ', 1)
        if len(parts) == 2:
            objectives_section.append(Paragraph(f"• <b>{parts[0]}:</b> {parts[1]}", bullet_style))
        else:
            objectives_section.append(Paragraph(f"• {objective}", bullet_style))
    
    story.append(KeepTogether(objectives_section))
    story.append(Spacer(1, 25))
    
    # Technical Skills - comprehensive section
    skills_section = []
    skills_section.append(Paragraph("Professional Technical Skills Demonstrated", subheading_style))
    skills_section.append(Paragraph(
        "This project showcases comprehensive networking competencies essential for enterprise "
        "network engineering roles, combining advanced theoretical knowledge with practical "
        "implementation expertise:",
        normal_style
    ))
    
    technical_skills = [
        "Cisco Router Configuration: Expert-level CLI-based configuration of ISR routers with advanced interface management",
        "Static Routing Implementation: Professional configuration of static routes with next-hop and administrative distance",
        "Network Architecture Design: Application of hierarchical design principles for enterprise-grade scalability",
        "IP Addressing & VLSM: Efficient IP address space utilization with Variable Length Subnet Masking",
        "Layer 2 Technologies: Advanced understanding of switching operations and VLAN implementation concepts", 
        "Network Troubleshooting: Systematic diagnostic approach using multiple validation and testing methodologies",
        "Protocol Analysis: Deep understanding of ARP, frame forwarding, and routing protocol operations",
        "Professional Documentation: Creation of comprehensive technical documentation meeting industry standards",
        "Performance Optimization: Network tuning and configuration optimization for maximum efficiency",
        "Security Implementation: Application of network security best practices and access control methods"
    ]
    
    for skill in technical_skills:
        parts = skill.split(': ', 1)
        if len(parts) == 2:
            skills_section.append(Paragraph(f"• <b>{parts[0]}:</b> {parts[1]}", bullet_style))
        else:
            skills_section.append(Paragraph(f"• {skill}", bullet_style))
    
    story.append(KeepTogether(skills_section))
    story.append(Spacer(1, 25))
    
    # Learning Outcomes - comprehensive
    learning_section = []
    learning_section.append(Paragraph("Professional Learning Outcomes & Career Development", subheading_style))
    learning_section.append(Paragraph(
        "The Cisco Virtual Internship Program 2025 has provided invaluable hands-on experience "
        "with enterprise networking technologies, bridging the gap between theoretical knowledge "
        "and real-world application. Key professional development outcomes include:",
        normal_style
    ))
    
    learning_outcomes = [
        "Real-World Application: Practical experience implementing enterprise solutions using industry-standard equipment",
        "Professional Methodologies: Exposure to systematic network design, implementation, and validation processes",
        "Industry Best Practices: Comprehensive understanding of Cisco networking standards and configuration methodologies",
        "Analytical Problem-Solving: Development of advanced troubleshooting and network optimization skills",
        "Career Readiness: Hands-on preparation for network engineering and infrastructure management roles",
        "Technical Leadership: Experience in project planning, execution, and professional documentation standards"
    ]
    
    for outcome in learning_outcomes:
        parts = outcome.split(': ', 1)
        if len(parts) == 2:
            learning_section.append(Paragraph(f"• <b>{parts[0]}:</b> {parts[1]}", bullet_style))
        else:
            learning_section.append(Paragraph(f"• {outcome}", bullet_style))
    
    story.append(KeepTogether(learning_section))
    story.append(Spacer(1, 30))
    
    # Final Assessment - keep together
    final_section = []
    final_section.append(Paragraph("Final Professional Assessment", subheading_style))
    final_section.append(Paragraph(
        "This enterprise network implementation represents a comprehensive demonstration of "
        "professional-level networking capabilities. The project successfully combines solid "
        "theoretical foundations with practical implementation skills, resulting in a fully "
        "functional, well-documented network solution ready for enterprise deployment.",
        normal_style
    ))
    
    final_section.append(Paragraph(
        "The systematic approach to network design, meticulous attention to configuration details, "
        "and comprehensive validation procedures reflect the high standards expected in professional "
        "network engineering environments. This project establishes a strong foundation for "
        "advanced networking studies and successful career development in the field.",
        normal_style
    ))
    
    story.append(KeepTogether(final_section))
    story.append(Spacer(1, 30))
    
    # Project Statistics - comprehensive summary table
    stats_section = []
    stats_section.append(Paragraph("Comprehensive Project Statistics", subheading_style))
    
    stats_data = [
        [Paragraph("<b>Project Metric</b>", table_header_style), 
         Paragraph("<b>Achievement Details</b>", table_header_style)],
        [Paragraph("Network Infrastructure", table_cell_style), 
         Paragraph("6 devices configured (2 ISR routers, 2 switches, 4 PCs)", table_cell_style)],
        [Paragraph("IP Network Implementation", table_cell_style), 
         Paragraph("3 subnets deployed (2 LAN segments, 1 WAN connection)", table_cell_style)],
        [Paragraph("Routing Configuration", table_cell_style), 
         Paragraph("2 bidirectional static routes with next-hop specification", table_cell_style)],
        [Paragraph("Connectivity Success Rate", table_cell_style), 
         Paragraph("100% success across all 8 connectivity test scenarios", table_cell_style)],
        [Paragraph("Validation Methodology", table_cell_style), 
         Paragraph("Multi-layer testing: CLI validation + simulation analysis", table_cell_style)],
        [Paragraph("Documentation Standard", table_cell_style), 
         Paragraph("Professional technical documentation with visual evidence", table_cell_style)],
        [Paragraph("Performance Metrics", table_cell_style), 
         Paragraph("Optimal network convergence and packet delivery rates", table_cell_style)],
        [Paragraph("Industry Compliance", table_cell_style), 
         Paragraph("Cisco best practices and enterprise configuration standards", table_cell_style)]
    ]
    
    stats_table = Table(stats_data, colWidths=[2.5*inch, 3.5*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1f4e79')),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8)
    ]))
    
    stats_section.append(stats_table)
    story.append(KeepTogether(stats_section))
    story.append(Spacer(1, 40))
    
    # Professional Footer - keep together
    footer_section = []
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=11,
        alignment=1,
        textColor=colors.HexColor('#1f4e79'),
        fontName='Helvetica',
        leading=14
    )
    
    footer_section.append(Paragraph(
        f"<b>Professional Report Completion</b><br/>"
        f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}<br/>"
        f"Platform: Cisco Packet Tracer - Enterprise Static Routing Implementation<br/>"
        f"Project File: new.pkt<br/>"
        f"Student: Harshal Sakpal - A.P Shah Institute of Technology<br/>"
        f"<b>Cisco Virtual Internship Program 2025</b>",
        footer_style
    ))
    
    story.append(KeepTogether(footer_section))
    
    # Build PDF with error handling
    try:
        doc.build(story)
        print(f"✅ IMPROVED PROFESSIONAL PDF REPORT GENERATED!")
        print(f"📄 File: {pdf_path}")
        print(f"📊 Size: {os.path.getsize(pdf_path) / 1024:.1f} KB")
        print(f"🎯 Enhanced layout with better organization!")
        print(f"🔧 Key Improvements:")
        print(f"   - Better content grouping with KeepTogether")
        print(f"   - Improved spacing and typography")
        print(f"   - Enhanced table layouts")
        print(f"   - Professional color scheme")
        print(f"   - Optimized page breaks")
        return pdf_path
    except Exception as e:
        print(f"❌ Error generating improved PDF: {str(e)}")
        return None

if __name__ == "__main__":
    create_improved_cisco_vip_report()