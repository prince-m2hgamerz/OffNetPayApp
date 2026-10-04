package com.offnetpay.app.presentation.ui.theme

import androidx.compose.ui.graphics.Color

/**
 * FamPay-inspired palette: warm white canvas, vibrant yellow accent,
 * rounded friendly surfaces, and dark text for high readability.
 */
object NeoPopColors {
    // Surface
    val Black        = Color(0xFF1A1A2E)   // deep navy (used for status bar)
    val Surface      = Color(0xFFFFFFFF)   // pure white card surface
    val SurfaceHigh  = Color(0xFFF7F7FB)   // very light grey card
    val SurfaceHigher= Color(0xFFEEEEF6)   // slightly darker card

    // Borders
    val Border       = Color(0xFFE0E0EE)
    val BorderStrong = Color(0xFFCCCCDD)

    // Text
    val TextPrimary   = Color(0xFF1A1A2E)  // deep navy text
    val TextSecondary = Color(0xFF5C5C7A)
    val TextMuted     = Color(0xFF9E9EB8)

    // Accent — FamPay signature yellow
    val Accent    = Color(0xFFFFBF00)
    val AccentDim = Color(0xFFE5AC00)
    val AccentDeep= Color(0xFFC49400)

    // Status
    val Danger    = Color(0xFFFF4D4D)
    val DangerDim = Color(0xFFB23636)
    val DangerDeep= Color(0xFF6B1F1F)

    val Success   = Color(0xFF00C853)
    val SuccessDim= Color(0xFF008E3A)
    val SuccessDeep = Color(0xFF00541F)

    val Warn    = Color(0xFFFFBF00)
    val WarnDim = Color(0xFFB38600)

    val Overlay = Color(0x661A1A2E)
}
