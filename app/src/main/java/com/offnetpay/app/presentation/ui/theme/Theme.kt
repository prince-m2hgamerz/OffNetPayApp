package com.offnetpay.app.presentation.ui.theme

import android.app.Activity
import android.os.Build
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val FamPayColorScheme = lightColorScheme(
    primary             = NeoPopColors.Accent,
    onPrimary           = NeoPopColors.TextPrimary,
    primaryContainer    = NeoPopColors.AccentDim,
    onPrimaryContainer  = NeoPopColors.TextPrimary,
    secondary           = NeoPopColors.TextSecondary,
    onSecondary         = NeoPopColors.Surface,
    background          = NeoPopColors.SurfaceHigh,
    onBackground        = NeoPopColors.TextPrimary,
    surface             = NeoPopColors.Surface,
    onSurface           = NeoPopColors.TextPrimary,
    surfaceVariant      = NeoPopColors.SurfaceHigher,
    onSurfaceVariant    = NeoPopColors.TextSecondary,
    error               = NeoPopColors.Danger,
    onError             = NeoPopColors.Surface,
    outline             = NeoPopColors.Border,
    outlineVariant      = NeoPopColors.BorderStrong
)

/**
 * FamPay-inspired light theme — clean white surfaces, navy text, yellow CTA.
 */
@Composable
fun OffNetPayTheme(content: @Composable () -> Unit) {
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = NeoPopColors.Surface.toArgb()
            window.navigationBarColor = NeoPopColors.SurfaceHigh.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = true
            WindowCompat.getInsetsController(window, view).isAppearanceLightNavigationBars = true
        }
    }
    MaterialTheme(
        colorScheme = FamPayColorScheme,
        typography = NeoPopTypography,
        shapes = NeoPopShapes,
        content = content
    )
}
