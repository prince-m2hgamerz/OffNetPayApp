package com.offnetpay.app.presentation

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import com.offnetpay.app.presentation.navigation.OffNetPayApp
import com.offnetpay.app.presentation.ui.theme.NeoPopColors
import com.offnetpay.app.presentation.ui.theme.OffNetPayTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Activity launched under Theme.OffNetPay.Splash; swap to the real
        // theme so edge-to-edge colours and statusBar transparency apply.
        // On API 31+ the system splash composes from windowSplashScreen*
        // attributes in values-v31/themes.xml and dismisses itself once
        // the first window is drawn — no extra library needed.
        setTheme(com.offnetpay.app.R.style.Theme_OffNetPay)
        enableEdgeToEdge()
        setContent {
            OffNetPayTheme {
                Box(
                    Modifier
                        .fillMaxSize()
                        .background(NeoPopColors.Black)
                ) {
                    OffNetPayApp()
                }
            }
        }
    }
}
