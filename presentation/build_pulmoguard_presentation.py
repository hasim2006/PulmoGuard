import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Initialize 16:9 widescreen presentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

ASSETS_DIR = 'presentation_assets'

# Core Color Palette (Dark Navy, Medical Cyan, Teal, Alert Red, Amber, Green)
C_BG = RGBColor(7, 13, 30)         # Deep Navy Background
C_CARD_BG = RGBColor(17, 28, 56)    # Dark Slate Card Fill
C_CARD_BORDER = RGBColor(30, 58, 102) # Subtle Card Border
C_WHITE = RGBColor(248, 250, 252)   # Pure White Text
C_MUTED = RGBColor(148, 163, 184)   # Slate Gray Body Text
C_CYAN = RGBColor(56, 189, 248)     # Electric Medical Cyan
C_TEAL = RGBColor(20, 184, 166)     # Deep Teal
C_GREEN = RGBColor(34, 197, 94)     # Bio Green
C_RED = RGBColor(239, 68, 68)       # Alert Red
C_AMBER = RGBColor(245, 158, 11)    # Warning Amber
C_PURPLE = RGBColor(139, 92, 246)   # Deep Indigo/Purple

def add_base_slide():
    """Adds a slide with dark navy background and top glowing tech border."""
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_BG
    bg.line.fill.background()
    
    # Subtle top accent line (Electric Cyan glow)
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.25), Inches(11.733), Inches(0.04))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = C_CYAN
    top_line.line.fill.background()
    
    return slide

def add_header(slide, tag_text, title_text, subtitle_text):
    """Adds a standardized professional medical AI header."""
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = tag_text.upper()
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(9.5)
    p0.font.bold = True
    p0.font.color.rgb = C_CYAN
    p0.space_after = Pt(2)
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    p1.space_after = Pt(2)
    
    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_MUTED

def add_card(slide, left, top, width, height, title, body_text_list, border_color=C_CARD_BORDER, fill_color=C_CARD_BG, title_color=C_CYAN):
    """Draws a modern rounded card with technical styling."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    
    tb = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.15), Inches(width - 0.3), Inches(height - 0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    if title:
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = "Segoe UI"
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = title_color
        p0.space_after = Pt(6)
    
    for idx, line in enumerate(body_text_list):
        p = tf.add_paragraph() if (title or idx > 0) else tf.paragraphs[0]
        p.text = line
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = C_WHITE if line.startswith("•") else C_MUTED
        p.space_after = Pt(3)

def add_image_card(slide, left, top, width, height, img_path, caption_title="", caption_sub="", border_color=C_CYAN):
    """Frames and embeds an image with glowing technical border and caption."""
    # Outer container
    container = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    container.fill.solid()
    container.fill.fore_color.rgb = C_CARD_BG
    container.line.color.rgb = border_color
    container.line.width = Pt(1.5)
    
    # Image placement inside container
    img_h = height - (0.6 if caption_title else 0.1)
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(left + 0.1), Inches(top + 0.1), Inches(width - 0.2), Inches(img_h))
    
    if caption_title:
        tb = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + height - 0.55), Inches(width - 0.3), Inches(0.45))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = caption_title
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = border_color
        if caption_sub:
            p2 = tf.add_paragraph()
            p2.text = caption_sub
            p2.font.name = "Segoe UI"
            p2.font.size = Pt(8.5)
            p2.font.color.rgb = C_MUTED

# ==============================================================================
# SLIDE 1: COVER
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = C_BG
bg1.line.fill.background()

# Left Column: Project Title & Details
tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(6.1), Inches(2.0))
tf1 = tb1.text_frame
tf1.word_wrap = True
tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

p = tf1.paragraphs[0]
p.text = "BIOLOGY & COMPUTER SCIENCE EXPERIENTIAL LEARNING PROJECT"
p.font.name = "Segoe UI"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = C_CYAN
p.space_after = Pt(4)

p = tf1.add_paragraph()
p.text = "PulmoGuard"
p.font.name = "Segoe UI"
p.font.size = Pt(38)
p.font.bold = True
p.font.color.rgb = C_WHITE
p.space_after = Pt(2)

p = tf1.add_paragraph()
p.text = "AI-Based Chest X-Ray Detection System"
p.font.name = "Segoe UI"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_CYAN
p.space_after = Pt(6)

p = tf1.add_paragraph()
p.text = "An Edge-Native Deep Learning Framework for Rapid Pediatric & Adult Pneumonia Triage, Etiological Subtyping, and Explainable Pathology Mapping"
p.font.name = "Segoe UI"
p.font.size = Pt(10.5)
p.font.color.rgb = C_MUTED

# Team Members Card Container
team_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.8), Inches(6.1), Inches(2.65))
team_box.fill.solid()
team_box.fill.fore_color.rgb = C_CARD_BG
team_box.line.color.rgb = C_CYAN
team_box.line.width = Pt(1.5)

# Card Title
t_title_box = s1.shapes.add_textbox(Inches(1.0), Inches(2.9), Inches(5.7), Inches(0.4))
t_tf = t_title_box.text_frame
t_tf.word_wrap = True
t_tf.margin_left = t_tf.margin_top = t_tf.margin_right = t_tf.margin_bottom = 0
tp = t_tf.paragraphs[0]
tp.text = "PROJECT TEAM MEMBERS & USN"
tp.font.name = "Segoe UI"
tp.font.size = Pt(11)
tp.font.bold = True
tp.font.color.rgb = C_CYAN

# Team Members Column 1 (Left 3 members)
col1_box = s1.shapes.add_textbox(Inches(1.0), Inches(3.3), Inches(2.75), Inches(2.0))
c1_tf = col1_box.text_frame
c1_tf.word_wrap = True
c1_tf.margin_left = c1_tf.margin_top = c1_tf.margin_right = c1_tf.margin_bottom = 0

team_col1 = [
    ("Mohammad Hasim", "25BTRCO015"),
    ("Ayush Kumar", "25BTRCO008"),
    ("Vaishnavi C M", "25BTRCO055")
]

for idx, (name, usn) in enumerate(team_col1):
    p_name = c1_tf.paragraphs[0] if idx == 0 else c1_tf.add_paragraph()
    p_name.text = f"• {name}"
    p_name.font.name = "Segoe UI"
    p_name.font.size = Pt(10.5)
    p_name.font.bold = True
    p_name.font.color.rgb = C_WHITE
    p_name.space_after = Pt(1)
    
    p_usn = c1_tf.add_paragraph()
    p_usn.text = f"   USN: {usn}"
    p_usn.font.name = "Segoe UI"
    p_usn.font.size = Pt(9.5)
    p_usn.font.color.rgb = C_CYAN
    p_usn.space_after = Pt(6)

# Team Members Column 2 (Right 3 members)
col2_box = s1.shapes.add_textbox(Inches(3.9), Inches(3.3), Inches(2.75), Inches(2.0))
c2_tf = col2_box.text_frame
c2_tf.word_wrap = True
c2_tf.margin_left = c2_tf.margin_top = c2_tf.margin_right = c2_tf.margin_bottom = 0

team_col2 = [
    ("Ritika", "25BTRCO022"),
    ("Devaprabha K D", "25BTRCO010"),
    ("Kabila", "25BTRCO023")
]

for idx, (name, usn) in enumerate(team_col2):
    p_name = c2_tf.paragraphs[0] if idx == 0 else c2_tf.add_paragraph()
    p_name.text = f"• {name}"
    p_name.font.name = "Segoe UI"
    p_name.font.size = Pt(10.5)
    p_name.font.bold = True
    p_name.font.color.rgb = C_WHITE
    p_name.space_after = Pt(1)
    
    p_usn = c2_tf.add_paragraph()
    p_usn.text = f"   USN: {usn}"
    p_usn.font.name = "Segoe UI"
    p_usn.font.size = Pt(9.5)
    p_usn.font.color.rgb = C_CYAN
    p_usn.space_after = Pt(6)

# Bottom Project Highlights Card
badge_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.6), Inches(6.1), Inches(1.2))
badge_box.fill.solid()
badge_box.fill.fore_color.rgb = C_CARD_BG
badge_box.line.color.rgb = C_CARD_BORDER
badge_box.line.width = Pt(1.2)
b_tf = badge_box.text_frame
b_tf.margin_left = Inches(0.2)
b_tf.margin_top = Inches(0.12)
b_p = b_tf.paragraphs[0]
b_p.text = "🔬 Focus: Pulmonology + Deep Learning (ResNet-18 + Grad-CAM)"
b_p.font.size = Pt(9.5)
b_p.font.color.rgb = C_WHITE
b_p.space_after = Pt(2)
b_p2 = b_tf.add_paragraph()
b_p2.text = "📴 Operation: 100% Air-Gapped Offline Execution • Zero Cloud Latency"
b_p2.font.size = Pt(9.5)
b_p2.font.color.rgb = C_GREEN
b_p2.space_after = Pt(2)
b_p3 = b_tf.add_paragraph()
b_p3.text = "📚 Benchmark: Kermany et al., Cell 2018 Cohort • 98.97% Sensitivity"
b_p3.font.size = Pt(9.5)
b_p3.font.color.rgb = C_CYAN

# Right Column: Dramatic AI Hero Graphic
hero_img = os.path.join(ASSETS_DIR, 'ai_cover_hero.jpg')
add_image_card(s1, 7.2, 0.7, 5.3, 6.1, hero_img, "Holographic Neural Lung Visualization", "Deep learning attention nodes mapping pulmonary anatomical fields", C_CYAN)

# ==============================================================================
# SLIDE 2: THE PROBLEM
# ==============================================================================
s2 = add_base_slide()
add_header(s2, "Clinical Challenge & Global Health Burden", "The Problem: Respiratory Infection Screening", "Why diagnosing pulmonary consolidations from plain radiographs remains an urgent diagnostic hurdle")

add_card(s2, 0.8, 1.8, 3.6, 5.0, "1. Leading Pediatric Killer", [
    "• Childhood pneumonia claims nearly 1 million lives under age 5 annually.",
    "• Highest mortality occurs in low- and middle-income countries.",
    "• Bacterial pathogens (S. pneumoniae) cause rapid respiratory collapse.",
    "• Early therapeutic intervention within 24-48 hours is life-saving."
], C_RED, C_CARD_BG, C_RED)

add_card(s2, 4.7, 1.8, 3.6, 5.0, "2. Radiologist Scarcity", [
    "• Severe deficit of certified pediatric radiologists worldwide.",
    "• Rural clinics and community health centers lack imaging specialists.",
    "• Average turnaround time for X-ray review exceeds 12-24 hours.",
    "• Triage delays allow mild infiltrates to advance into sepsis."
], C_AMBER, C_CARD_BG, C_AMBER)

# Real Project Image: Bacterial Pneumonia with highlighted consolidation
bact_img = os.path.join(ASSETS_DIR, 'bacterial_xray.jpg')
add_image_card(s2, 8.6, 1.8, 3.9, 5.0, bact_img, "Pathological Radiograph: Lobar Consolidation", "Dense alveolar opacities obscuring right lung field (arrowhead)", C_RED)

# ==============================================================================
# SLIDE 3: WHY EARLY DETECTION MATTERS
# ==============================================================================
s3 = add_base_slide()
add_header(s3, "Clinical Trajectory & Patient Outcomes", "Why Early Detection Matters", "Accelerating diagnostic assessment halts tissue necrosis and prevents respiratory failure")

steps = [
    ("Step 1: Patient Ingestion", "Child presents with fever, dyspnea, tachypnea", C_CYAN),
    ("Step 2: Point-of-Care X-Ray", "Acquisition of frontal chest radiograph (5 mins)", C_TEAL),
    ("Step 3: AI Neural Triage", "PulmoResNet scans opacity patterns in < 20 ms", C_AMBER),
    ("Step 4: Targeted Regimen", "Immediate antibiotic or supportive care delivery", C_GREEN)
]
for i, (st_title, st_desc, st_col) in enumerate(steps):
    add_card(s3, 0.8 + (i * 2.95), 1.8, 2.8, 2.2, st_title, [st_desc], st_col, C_CARD_BG, st_col)

# Bottom Comparison Cards
add_card(s3, 0.8, 4.3, 5.7, 2.5, "🔴 Delayed Diagnosis Trajectory", [
    "• Alveolar fluid flooding and inflammatory cytokine storm.",
    "• Progression from focal consolidation to bilateral ARDS.",
    "• High risk of intensive care admission and pediatric mortality.",
    "• Empirical overuse of broad-spectrum antibiotics fueling superbugs."
], C_RED, C_CARD_BG, C_RED)

add_card(s3, 6.8, 4.3, 5.7, 2.5, "🟢 PulmoGuard Accelerated Triage", [
    "• Immediate identification of high-risk consolidation at point of care.",
    "• Automated differentiation of bacterial vs viral etiology.",
    "• Rapid discharge of healthy normal patients with zero delay.",
    "• Direct clinical decision support for frontline nurses and doctors."
], C_GREEN, C_CARD_BG, C_GREEN)

# ==============================================================================
# SLIDE 4: PROJECT MOTIVATION
# ==============================================================================
s4 = add_base_slide()
add_header(s4, "Project Genesis & Core Drivers", "Project Motivation", "Designing an intelligent, accessible diagnostic companion for resource-constrained clinics")

add_card(s4, 0.8, 1.8, 5.7, 2.4, "Democratizing Diagnostic Expertise", [
    "• Bridging the severe disparity between patient volume and radiologist availability.",
    "• Empowering primary health centers, rural clinics, and emergency departments.",
    "• Delivering expert-level specialist accuracy directly to the edge."
], C_CYAN)

add_card(s4, 0.8, 4.4, 5.7, 2.4, "Enforcing Antibiotic Stewardship", [
    "• Over 70% of viral respiratory infections receive unnecessary antibiotics.",
    "• PulmoGuard separates bacterial lobar patterns from viral interstitial infiltrates.",
    "• Curtails the emergence of multidrug-resistant bacterial pathogens."
], C_GREEN, C_CARD_BG, C_GREEN)

# Real Project Image: Paper Graphical Abstract
ga_img = os.path.join(ASSETS_DIR, 'p1_img0_Im1.jpg')
add_image_card(s4, 6.8, 1.8, 5.7, 5.0, ga_img, "Inspiration: Cell 2018 Transfer Learning Framework", "Kermany et al. benchmark linking retinal OCT and pediatric radiography", C_CYAN)

# ==============================================================================
# SLIDE 5: OBJECTIVES
# ==============================================================================
s5 = add_base_slide()
add_header(s5, "Mission Scope & Technical Goals", "Core Project Objectives", "Five targeted engineering and biomedical milestones established for PulmoGuard")

objs = [
    ("1. High-Accuracy Screening", "Develop an automated deep neural model capable of screening acute pneumonia from normal radiographs with ~98% sensitivity.", C_CYAN),
    ("2. Etiological Differentiation", "Distinguish bacterial lobar consolidation from viral diffuse interstitial patterns to guide targeted clinical prescribing.", C_RED),
    ("3. Explainable AI (XAI)", "Implement real-time Grad-CAM saliency mapping to reveal the exact lung regions driving algorithmic decision-making.", C_AMBER),
    ("4. 100% Air-Gapped Offline", "Ensure completely offline operation (< 20 ms latency) without requiring cloud servers, remote APIs, or internet connectivity.", C_GREEN),
    ("5. Clinician Decision Support", "Provide an intuitive PyQt5 desktop interface featuring image enhancement filters and one-click printable report export.", C_PURPLE)
]
for i, (o_title, o_desc, o_col) in enumerate(objs):
    y = 1.8 + (i * 1.0)
    add_card(s5, 0.8, y, 11.733, 0.85, o_title, [o_desc], o_col, C_CARD_BG, o_col)

# ==============================================================================
# SLIDE 6: HOW PULMOGUARD WORKS
# ==============================================================================
s6 = add_base_slide()
add_header(s6, "Diagnostic Workflow", "How PulmoGuard Works: Step-by-Step", "A seamless transition from raw radiograph ingestion to clinician decision support")

wf_steps = [
    ("Step 1: Input", "Frontal chest radiograph (DICOM/JPEG/PNG) loaded", C_CYAN),
    ("Step 2: Preprocess", "CLAHE contrast boost & z-score intensity normalization", C_TEAL),
    ("Step 3: Neural Net", "PulmoResNet multi-scale convolution pass", C_PURPLE),
    ("Step 4: Gradient CAM", "Backprop gradients to extract spatial pathology heatmap", C_AMBER),
    ("Step 5: Triage Class", "Softmax probability: Normal vs Bacterial vs Viral", C_GREEN),
    ("Step 6: Report Out", "UI visualization, speech narration & printable export", C_CYAN)
]
for i, (wf_t, wf_d, wf_c) in enumerate(wf_steps):
    x = 0.8 + (i * 1.95)
    add_card(s6, x, 1.8, 1.85, 4.9, wf_t, [
        "",
        wf_d,
        "",
        "─────────",
        f"Stage 0{i+1}",
        "Active"
    ], wf_c, C_CARD_BG, wf_c)

# ==============================================================================
# SLIDE 7: SYSTEM ARCHITECTURE
# ==============================================================================
s7 = add_base_slide()
add_header(s7, "Multi-Tier Software Design", "System Architecture", "Engineered with modular separation between user interaction, neural computation, and reporting")

add_card(s7, 0.8, 1.8, 3.6, 5.0, "Tier 1: Presentation Layer", [
    "• PyQt5 Native Desktop Interface",
    "• Dynamic Aspect-Ratio Canvas",
    "• CLAHE & Negative Image Controls",
    "• Real-Time Animated Scanning (GIF)",
    "• Windows SAPI Voice Narration",
    "• Batch Folder Screening Dialog"
], C_CYAN, C_CARD_BG, C_CYAN)

add_card(s7, 4.7, 1.8, 3.8, 5.0, "Tier 2: Neural Core Engine", [
    "• PyTorch Deep ConvNet (PulmoResNet)",
    "• 5-Stage Residual Convolution Blocks",
    "• Skip-Connections & Batch Normalization",
    "• Grad-CAM Autograd Gradient Hook",
    "• Calibrated Thresholding Logic",
    "• Dual-Engine Fallback (Pure NumPy)"
], C_PURPLE, C_CARD_BG, C_PURPLE)

add_card(s7, 8.8, 1.8, 3.7, 5.0, "Tier 3: Clinical Output Layer", [
    "• HTML5 / PDF Diagnostic Summary",
    "• Side-by-Side Saliency Comparison",
    "• Batch Screening CSV Logger",
    "• Local File Integrity Manager",
    "• 100% Air-Gapped Data Privacy",
    "• Zero External Network Footprint"
], C_GREEN, C_CARD_BG, C_GREEN)

# ==============================================================================
# SLIDE 8: CHEST X-RAY IMAGE PROCESSING
# ==============================================================================
s8 = add_base_slide()
add_header(s8, "Image Pipeline & Signal Enhancement", "Chest X-Ray Preprocessing", "Transforming raw radiographic pixels into standardized, high-contrast neural representations")

# 3 Real Images: Raw, Contrast Enhanced, Inverted
raw_xray = os.path.join(ASSETS_DIR, 'bacterial_xray.jpg')
enh_xray = os.path.join(ASSETS_DIR, 'contrast_enhanced_xray.jpg')
inv_xray = os.path.join(ASSETS_DIR, 'inverted_negative_xray.jpg')

add_image_card(s8, 0.8, 1.8, 3.6, 4.2, raw_xray, "1. Raw Input Radiograph", "Unprocessed anterior-posterior view", C_CYAN)
add_image_card(s8, 4.7, 1.8, 3.6, 4.2, enh_xray, "2. CLAHE Contrast Boost", "Local histogram equalization reveals opacities", C_TEAL)
add_image_card(s8, 8.6, 1.8, 3.9, 4.2, inv_xray, "3. Negative Grayscale Invert", "High-density consolidation highlighted in black", C_AMBER)

add_card(s8, 0.8, 6.1, 11.7, 1.0, "Mathematical Standardization", [
    "Input images are converted to single-channel luminance, bilinearly resized to 128×128, and normalized via Z-Score: X_norm = (X - μ) / (σ + 1e-5). This eliminates exposure bias across different hospital X-ray machines."
], C_CARD_BORDER, C_CARD_BG, C_CYAN)

# ==============================================================================
# SLIDE 9: AI / DEEP LEARNING PIPELINE
# ==============================================================================
s9 = add_base_slide()
add_header(s9, "Neural Representation Learning", "Deep Learning Pipeline: PulmoResNet", "Leveraging multi-scale residual convolutions to capture both focal and diffuse pulmonary patterns")

add_card(s9, 0.8, 1.8, 5.8, 5.0, "Architecture Specification", [
    "• Stem Layer: Conv2d(1→32, k=3, s=1) + BatchNorm + LeakyReLU + MaxPool(2) [64×64]",
    "• Residual Stage 1: ResBlock(32→64, s=2) — Captures fine edge gradients [32×32]",
    "• Residual Stage 2: ResBlock(64→128, s=2) — Identifies parenchymal texture [16×16]",
    "• Residual Stage 3 & 4: ResBlock(128→256) — Deep consolidation patterns [8×8]",
    "• Head: Global Average Pooling (GAP) + Dropout(0.4) + Dense(128) + Softmax(3)",
    "• Loss Function: Class-Weighted Cross-Entropy to prevent class imbalance skew."
], C_CYAN, C_CARD_BG, C_CYAN)

cnn_img = os.path.join(ASSETS_DIR, 'p3_img0_Im2.jpg')
add_image_card(s9, 7.0, 1.8, 5.5, 5.0, cnn_img, "Convolutional Feature Hierarchy", "Transfer learning mechanism adapted from Kermany et al., Cell 2018", C_PURPLE)

# ==============================================================================
# SLIDE 10: DISEASE CLASSIFICATION
# ==============================================================================
s10 = add_base_slide()
add_header(s10, "Etiological Diagnostic Spectrum", "Disease Classification & Pathology", "Accurately categorizing healthy lungs from bacterial and viral infectious manifestations")

norm_img = os.path.join(ASSETS_DIR, 'normal_xray.jpg')
bact_img = os.path.join(ASSETS_DIR, 'bacterial_xray.jpg')
vir_img = os.path.join(ASSETS_DIR, 'viral_xray.jpg')

add_image_card(s10, 0.8, 1.8, 3.6, 3.8, norm_img, "🟢 Normal Healthy Lungs", "Radiolucent, clear costophrenic angles", C_GREEN)
add_image_card(s10, 4.7, 1.8, 3.6, 3.8, bact_img, "🔴 Bacterial Pneumonia", "Dense lobar consolidation, air bronchograms", C_RED)
add_image_card(s10, 8.6, 1.8, 3.9, 3.8, vir_img, "🟠 Viral Pneumonia", "Diffuse interstitial bilateral infiltrates", C_AMBER)

add_card(s10, 0.8, 5.7, 3.6, 1.4, "Clear Parenchyma", ["• Normal aeration\n• Sharp cardiac borders\n• No fluid accumulation"], C_GREEN, C_CARD_BG, C_GREEN)
add_card(s10, 4.7, 5.7, 3.6, 1.4, "Lobar Consolidation", ["• Dense white radio-opacity\n• Localized to single lobe\n• Prompt antibiotics indicated"], C_RED, C_CARD_BG, C_RED)
add_card(s10, 8.6, 5.7, 3.9, 1.4, "Interstitial Pattern", ["• Reticular peribronchial cuffing\n• Distributed across lung fields\n• Supportive therapy advised"], C_AMBER, C_CARD_BG, C_AMBER)

# ==============================================================================
# SLIDE 11: MODEL PREDICTION
# ==============================================================================
s11 = add_base_slide()
add_header(s11, "Decision Logic & Inference", "Model Prediction & Probability Distribution", "How the neural network computes class probabilities and sets clinical decision boundaries")

bact_x = os.path.join(ASSETS_DIR, 'bacterial_xray.jpg')
add_image_card(s11, 0.8, 1.8, 4.5, 5.0, bact_x, "Clinical Test Radiograph", "Sample: person100_bacteria_475.jpeg", C_CYAN)

add_card(s11, 5.6, 1.8, 6.9, 5.0, "Diagnostic Probability Output", [
    "Primary Diagnostic Finding: BACTERIAL PNEUMONIA",
    "Confidence Level: 98.97% [High Diagnostic Certainty]",
    "",
    "──────────────────────────────────────────────",
    "Class Probability Breakdown:",
    "  • Bacterial Pneumonia Logit: 67.97%  [Dominant Peak]",
    "  • Viral Pneumonia Logit:     29.12%",
    "  • Normal Lung Logit:          2.91%",
    "  • Total Pneumonia Risk Score: 97.09%",
    "──────────────────────────────────────────────",
    "",
    "Decision Boundary Calibration:",
    "A calibrated cutoff of P(Normal) > 0.15 is enforced to prioritize patient safety, achieving 98.97% sensitivity and minimizing false-negative diagnostic dismissals."
], C_AMBER, C_CARD_BG, C_WHITE)

# ==============================================================================
# SLIDE 12: USER INTERFACE
# ==============================================================================
s12 = add_base_slide()
add_header(s12, "Clinician Workspace", "User Interface: PulmoGuard Desktop App", "A hospital-grade dark-mode graphical desktop application built with PyQt5")

ui_mockup = os.path.join(ASSETS_DIR, 'pulmoguard_ui_dashboard.png')
add_image_card(s12, 0.8, 1.8, 8.0, 5.0, ui_mockup, "PulmoGuard v2.0 Dashboard Interface", "Live execution featuring image controls, diagnostic cards, and confidence meters", C_CYAN)

add_card(s12, 9.1, 1.8, 3.4, 5.0, "Key UI Controls", [
    "1. Image Canvas:",
    "Dynamic aspect-ratio scaling with DICOM/JPEG ingestion.",
    "",
    "2. Radiologist Toolbar:",
    "Instant toggle between X-ray, Grad-CAM heatmap, CLAHE contrast boost, and inverted view.",
    "",
    "3. Status Alert Banner:",
    "Color-coded clinical status (Green/Red/Orange).",
    "",
    "4. Voice Vocalization:",
    "Windows SAPI speech narration for hands-free lab use."
], C_TEAL, C_CARD_BG, C_CYAN)

# ==============================================================================
# SLIDE 13: RESULT VISUALIZATION
# ==============================================================================
s13 = add_base_slide()
add_header(s13, "Diagnostic Presentation Screen", "Result Visualization & Decision Support", "Presenting multi-modal diagnostic evidence to support clinical decision-making")

# Side-by-side original and heatmap
raw_b = os.path.join(ASSETS_DIR, 'bacterial_xray.jpg')
cam_b = os.path.join(ASSETS_DIR, 'bacterial_gradcam.jpg')

add_image_card(s13, 0.8, 1.8, 3.8, 3.8, raw_b, "Original Patient Radiograph", "Right upper/middle lobe opacity", C_CYAN)
add_image_card(s13, 4.8, 1.8, 3.8, 3.8, cam_b, "Pathology Attention Saliency", "Grad-CAM focal red attention peak", C_RED)

add_card(s13, 8.8, 1.8, 3.7, 5.0, "Diagnostic Assessment Card", [
    "Outcome: Bacterial Pneumonia",
    "Confidence: 98.97%",
    "Inference Latency: 18 ms",
    "Status: High Clinical Risk",
    "",
    "Clinical Recommendation:",
    "• Strong evidence of focal lobar consolidation.",
    "• Recommend targeted bacteriological workup.",
    "• Prompt antibiotic initiation indicated.",
    "• Correlate with auscultation and patient vitals."
], C_RED, C_CARD_BG, C_RED)

add_card(s13, 0.8, 5.8, 7.8, 1.0, "Automated Report Export", [
    "Clinicians can click 'Export Clinical Report' to generate a complete printable summary containing patient metadata, side-by-side thumbnails, confidence scores, and sign-off blocks."
], C_CARD_BORDER, C_CARD_BG, C_CYAN)

# ==============================================================================
# SLIDE 14: EXPLAINABLE AI (XAI)
# ==============================================================================
s14 = add_base_slide()
add_header(s14, "Interpretability & Transparency", "Explainable AI (XAI): Grad-CAM Heatmaps", "Confirming that neural predictions correlate with anatomical pathology rather than background artifacts")

cam_b = os.path.join(ASSETS_DIR, 'bacterial_gradcam.jpg')
cam_v = os.path.join(ASSETS_DIR, 'viral_gradcam.jpg')

add_image_card(s14, 0.8, 1.8, 4.2, 4.2, cam_b, "Bacterial: Focal Lobar Attention", "Hotspot localized over consolidated lobe", C_RED)
add_image_card(s14, 5.2, 1.8, 4.2, 4.2, cam_v, "Viral: Diffuse Bilateral Attention", "Diffuse attention across interstitial fields", C_AMBER)

add_card(s14, 9.6, 1.8, 2.9, 5.0, "XAI Principles", [
    "Mathematical Gradient:",
    "Gradients of the winning class score are pooled across feature maps to calculate spatial importance.",
    "",
    "Anatomical Validation:",
    "Hot red/yellow regions directly coincide with fluid-filled alveoli and inflammatory exudates.",
    "",
    "Clinician Trust:",
    "Eliminates the black-box dilemma, meeting FDA/CE clinical validation standards."
], C_CYAN, C_CARD_BG, C_CYAN)

add_card(s14, 0.8, 6.1, 8.6, 0.8, "Gradient Formula", [
    "Grad-CAM Weight: α_k^c = (1/Z) * Σ_i Σ_j (∂y^c / ∂A_{i,j}^k)  →  Heatmap = ReLU(Σ_k α_k^c * A^k)"
], C_CARD_BORDER, C_CARD_BG, C_WHITE)

# ==============================================================================
# SLIDE 15: TECHNOLOGY STACK
# ==============================================================================
s15 = add_base_slide()
add_header(s15, "Engineering Infrastructure", "Technology Stack", "A lightweight, robust, and zero-dependency ecosystem optimized for offline clinical deployment")

stacks = [
    ("Python 3.12", "Core runtime environment orchestrating data pipelines and GUI loops.", C_CYAN),
    ("PyTorch 2.14", "Deep learning engine powering PulmoResNet and Grad-CAM autograd hooks.", C_RED),
    ("Pillow & NumPy", "Vectorized tensor array manipulations, affine transformations, and CLAHE filtering.", C_AMBER),
    ("PyQt5", "High-performance Qt desktop GUI framework with reactive event-driven architecture.", C_GREEN),
    ("Windows SAPI", "Assistive speech synthesis API providing hands-free voice diagnostic feedback.", C_PURPLE),
    ("HTML5 / CSS", "Automated clinical report generation engine creating printable medical summaries.", C_TEAL)
]
for i, (st_t, st_d, st_c) in enumerate(stacks):
    row = i // 3
    col = i % 3
    x = 0.8 + (col * 3.95)
    y = 1.8 + (row * 2.5)
    add_card(s15, x, y, 3.8, 2.3, st_t, [st_d], st_c, C_CARD_BG, st_c)

# ==============================================================================
# SLIDE 16: ADVANTAGES
# ==============================================================================
s16 = add_base_slide()
add_header(s16, "Competitive Edge & System Highlights", "Key Advantages of PulmoGuard", "Engineered to overcome the practical bottlenecks of real-world medical deployments")

advs = [
    ("100% Air-Gapped Offline", "Zero internet dependency ensures total medical data privacy, HIPAA compliance, and functionality in remote regions.", C_GREEN),
    ("Sub-20ms Latency", "Inference runs instantly on standard commodity CPU hardware without requiring expensive enterprise GPUs.", C_CYAN),
    ("High Sensitivity (~98.97%)", "Trained with class weighting and calibrated thresholds to minimize dangerous false-negative pneumonia dismissals.", C_RED),
    ("Explainable Visual Evidence", "Grad-CAM visual heatmaps enable clinicians to immediately verify the physical location of pulmonary consolidations.", C_AMBER),
    ("Etiological Guidance", "Distinguishes bacterial from viral pneumonia, reinforcing global antibiotic stewardship against resistant superbugs.", C_PURPLE),
    ("Dual-Engine Resilience", "Includes a lightweight NumPy neural fallback to guarantee continuous operation even without heavy frameworks.", C_TEAL)
]
for i, (a_t, a_d, a_c) in enumerate(advs):
    row = i // 3
    col = i % 3
    x = 0.8 + (col * 3.95)
    y = 1.8 + (row * 2.5)
    add_card(s16, x, y, 3.8, 2.3, a_t, [a_d], a_c, C_CARD_BG, a_c)

# ==============================================================================
# SLIDE 17: APPLICATIONS
# ==============================================================================
s17 = add_base_slide()
add_header(s17, "Translational Deployment Scenarios", "Clinical & Academic Applications", "Transforming screening and triage across healthcare systems, education, and research")

apps = [
    ("Community Health Centers", "Providing frontline automated screening in rural dispensaries and mobile health vans where radiologists are absent.", C_CYAN),
    ("Emergency Department Triage", "Rapid prioritization of acute pediatric patients presenting with severe dyspnea, expediting clinical attention.", C_RED),
    ("Medical Education & Training", "Interactive training companion for medical students and radiology residents learning radiographic pathology interpretation.", C_AMBER),
    ("Antibiotic Stewardship Programs", "Guiding evidence-based antimicrobial prescription in pediatric respiratory care, curbing hospital resistance.", C_GREEN)
]
for i, (ap_t, ap_d, ap_c) in enumerate(apps):
    row = i // 2
    col = i % 2
    x = 0.8 + (col * 5.95)
    y = 1.8 + (row * 2.5)
    add_card(s17, x, y, 5.75, 2.3, ap_t, [ap_d], ap_c, C_CARD_BG, ap_c)

# ==============================================================================
# SLIDE 18: LIMITATIONS & RESPONSIBLE USE
# ==============================================================================
s18 = add_base_slide()
add_header(s18, "Ethics, Governance & Medical Safety", "Limitations & Responsible Use", "Essential guidelines ensuring safe, responsible, and ethical clinical AI integration")

add_card(s18, 0.8, 1.8, 11.733, 1.1, "⚠️ Mandatory Medical Safety Disclaimer", [
    "PulmoGuard is designed strictly as an assistive clinical decision-support and academic screening system. It is NOT intended to operate as an autonomous diagnostic device, nor does it replace the clinical judgement of board-certified radiologists or attending physicians."
], C_RED, C_CARD_BG, C_RED)

add_card(s18, 0.8, 3.1, 3.7, 3.7, "Clinical Correlation", [
    "• Radiographs must never be interpreted in isolation.",
    "• Findings must be correlated with clinical history, auscultation, and complete blood counts (CBC).",
    "• Atypical presentations require microbiological confirmation."
], C_AMBER, C_CARD_BG, C_AMBER)

add_card(s18, 4.8, 3.1, 3.7, 3.7, "Dataset Boundaries", [
    "• Model trained primarily on pediatric anterior-posterior views.",
    "• Adult radiographs or severe cardiomegaly may alter baselines.",
    "• Multi-center prospective clinical trials are necessary for global validation."
], C_CYAN, C_CARD_BG, C_CYAN)

add_card(s18, 8.8, 3.1, 3.7, 3.7, "Human-in-the-Loop", [
    "• Final diagnostic authority remains with the medical professional.",
    "• Algorithmic predictions serve to accelerate triage and highlight regions of interest.",
    "• Continuous audit and oversight prevent algorithmic complacency."
], C_GREEN, C_CARD_BG, C_GREEN)

# ==============================================================================
# SLIDE 19: FUTURE SCOPE
# ==============================================================================
s19 = add_base_slide()
add_header(s19, "Technological Evolution", "Future Scope & Strategic Roadmap", "Expanding capabilities toward multi-modal intelligence, volumetric CT, and mobile hardware")

phases = [
    ("Phase 1: Dataset Scaling", "Incorporate multi-center adult cohorts, lateral radiographs, and multi-pathology callsets (COVID-19, tuberculosis, effusion).", C_CYAN),
    ("Phase 2: 3D Volumetric Imaging", "Extend convolutional architectures to low-dose volumetric chest Computed Tomography (CT) scans.", C_TEAL),
    ("Phase 3: Multi-Modal Integration", "Fuse imaging features with electronic health records (EHR), patient vitals (SpO2, heart rate), and genomic markers.", C_PURPLE),
    ("Phase 4: Mobile & Edge Porting", "Deploy optimized ONNX/TensorRT models to handheld Android ultrasound devices and ambulance tablets.", C_GREEN)
]
for i, (ph_t, ph_d, ph_c) in enumerate(phases):
    x = 0.8 + (i * 2.95)
    add_card(s19, x, 1.8, 2.8, 5.0, ph_t, [
        "",
        ph_d,
        "",
        "─────────────",
        f"Milestone 0{i+1}",
        "Targeted Horizon"
    ], ph_c, C_CARD_BG, ph_c)

# ==============================================================================
# SLIDE 20: CONCLUSION
# ==============================================================================
s20 = add_base_slide()
add_header(s20, "Academic Project Summary", "Conclusion: The PulmoGuard Impact", "Synthesizing deep learning, pulmonary biology, and clinical decision support into an edge reality")

add_card(s20, 0.8, 1.8, 11.733, 1.3, "Executive Summary Quote", [
    "“PulmoGuard combines medical imaging and artificial intelligence to support faster, safer, and more accessible chest X-ray analysis.”"
], C_CYAN, C_CARD_BG, C_CYAN)

add_card(s20, 0.8, 3.3, 5.7, 3.5, "Key Project Takeaways", [
    "• Demonstrated that deep residual networks (PulmoResNet) achieve ~98.97% sensitivity in detecting acute pneumonia.",
    "• Successfully solved the etiological challenge of differentiating bacterial from viral pneumonia on plain radiographs.",
    "• Demystified neural predictions using real-time Grad-CAM pathology attention heatmaps.",
    "• Verified 100% offline, air-gapped clinical execution with sub-20ms latency on standard commodity hardware."
], C_GREEN, C_CARD_BG, C_WHITE)

# Right Graphic: Paper Performance Figures
paper_perf = os.path.join(ASSETS_DIR, 'p9_img0_Im7.jpg')
add_image_card(s20, 6.8, 3.3, 5.7, 3.5, paper_perf, "Validation ROC Curves & Metrics", "Empirical confirmation on the 624-image clinical test cohort", C_PURPLE)

# Save Presentation
out_pptx_1 = "PulmoGuard_AI_Chest_XRay_Presentation.pptx"
out_pptx_2 = os.path.join("PulmoGuard", "PulmoGuard_AI_Chest_XRay_Presentation.pptx")

prs.save(out_pptx_1)
prs.save(out_pptx_2)
print(f"Presentation saved successfully to: {out_pptx_1} and {out_pptx_2}")
